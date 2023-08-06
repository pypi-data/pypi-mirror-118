#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import importlib
import time
import pytz
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from autotrader.emailing import emailing
from autotrader.lib import autodata, environment_manager
from autotrader.lib.read_yaml import read_yaml


class AutoTraderBot():
    '''
    AutoTrader Bot.
    ---------------
    
    Attributes
    ----------
    broker : class
        The broker class instance.
        
    instrument : str
        The instrument being traded by the bot.
    
    strategy : class
         The strategy being traded by the bot.
    

    Methods
    -------
    update(i):
        Update strategy with latest data and generate latest signal.
    
    '''
    
    def __init__(self, instrument, strategy_config, broker, autotrader_attributes):
        '''
        AutoTrader Bot initialisation. 
        '''

        # Inherit user options from autotrader
        self.home_dir           = autotrader_attributes.home_dir
        self.scan_mode          = autotrader_attributes.scan_mode
        self.scan_index         = autotrader_attributes.scan_index
        self.scan_results       = {}
        self.broker_utils       = autotrader_attributes.broker_utils
        self.email_params       = autotrader_attributes.email_params
        self.notify             = autotrader_attributes.notify
        self.validation_file    = autotrader_attributes.validation_file
        self.verbosity          = autotrader_attributes.verbosity
        self.order_summary_fp   = autotrader_attributes.order_summary_fp
        self.backtest_mode      = autotrader_attributes.backtest_mode
        self.data_start         = autotrader_attributes.data_start
        self.data_end           = autotrader_attributes.data_end
        self.base_currency      = autotrader_attributes.backtest_base_currency
        self.environment        = autotrader_attributes.environment
        self.feed               = autotrader_attributes.feed
        self.data_file          = autotrader_attributes.data_file
        self.optimise_mode      = autotrader_attributes.optimise_mode
        self.include_broker     = autotrader_attributes.include_broker
        self.check_data_alignment = autotrader_attributes.check_data_alignment
        self.allow_dancing_bears = autotrader_attributes.allow_dancing_bears
        
        self.instrument         = instrument
        self.broker             = broker
        
        # Unpack strategy parameters
        interval                = strategy_config["INTERVAL"]
        period                  = strategy_config["PERIOD"]
        risk_pc                 = strategy_config["RISK_PC"]
        sizing                  = strategy_config["SIZING"] if 'SIZING' in strategy_config else 0
        params                  = strategy_config["PARAMETERS"]
        
        strategy_params                 = params
        strategy_params['granularity']  = interval
        strategy_params['risk_pc']      = risk_pc
        strategy_params['sizing']       = sizing
        strategy_params['period']       = period
        self.strategy_params            = strategy_params
        
        # Import Strategy
        strat_module            = strategy_config["MODULE"]
        strat_name              = strategy_config["CLASS"]
        strat_package_path      = os.path.join(self.home_dir, "strategies") 
        strat_module_path       = os.path.join(strat_package_path, strat_module) + '.py'
        strat_spec              = importlib.util.spec_from_file_location(strat_module, strat_module_path)
        strategy_module         = importlib.util.module_from_spec(strat_spec)
        strat_spec.loader.exec_module(strategy_module)
        strategy                = getattr(strategy_module, strat_name)
        
        # Get data
        global_config_fp = os.path.join(self.home_dir, 'config', 'GLOBAL.yaml')
        if os.path.isfile(global_config_fp):
            global_config = read_yaml(global_config_fp)
        else:
            global_config = None
        broker_config           = environment_manager.get_config(self.environment,
                                                             global_config,
                                                             self.feed)
        
        self.get_data           = autodata.GetData(broker_config, self.allow_dancing_bears)
        data, quote_data        = self._retrieve_data(instrument, self.feed)
        
        # instantiate strategy
        # my_strat = strategy(params, data, instrument)
        
        if self.include_broker:
            # my_strat.broker = self.broker
            # my_strat.broker_utils = self.broker_utils
            my_strat = strategy(params, data, instrument, self.broker, self.broker_utils)
        else:
            my_strat = strategy(params, data, instrument)
            
                
        self.strategy           = my_strat
        self.data               = data
        self.quote_data         = quote_data
        
        self.latest_orders      = []
        
        
        if int(self.verbosity) > 0:
                print("AutoTraderBot assigned to analyse {}".format(instrument),
                      "on {} timeframe using {}.".format(self.strategy_params['granularity'],
                                                         strategy_config['NAME']))
    
    def _update_strategy_data(self):
        '''
        Method to update strategy with latest data. Called by the bot manager.
        '''
        
        print("Updating strategy with latest data.")
        
        # TODO - add option to get dancing bears in autodata
        
        # Download new data
        new_data, _ = self._retrieve_data(self.instrument, self.feed)
        
        # Update strategy with new data
        self.strategy.initialise_strategy(new_data)
        
    
    def _retrieve_data(self, instrument, feed):
        '''
        Retrieves price data from AutoData.
        '''
    
        interval    = self.strategy_params['granularity']
        period      = self.strategy_params['period']
        price_data_path = os.path.join(self.home_dir, 'price_data')
        
        if self.backtest_mode is True:
            # Running in backtest mode
            self.get_data.base_currency = self.base_currency
            
            from_date       = self.data_start
            to_date         = self.data_end
            
            if self.validation_file is not None:
                # Extract instrument-specific trade history as trade summary and trade period
                livetrade_history = self.livetrade_history
                formatted_instrument = instrument[:3] + "/" + instrument[-3:]
                raw_livetrade_summary = livetrade_history[livetrade_history.Instrument == formatted_instrument] # FOR OANDA
                from_date           = pd.to_datetime(raw_livetrade_summary.Date.values)[0]
                to_date             = pd.to_datetime(raw_livetrade_summary.Date.values)[-1]
                
                self.raw_livetrade_summary = raw_livetrade_summary
                
                # Modify from date to improve backtest
                from_date = from_date - period*timedelta(seconds = self.granularity_to_seconds(interval))
                
                # Modify starting balance
                self.broker.portfolio_balance = raw_livetrade_summary.Balance.values[np.isfinite(raw_livetrade_summary.Balance.values)][0]
                
            if self.data_file is not None:
                custom_data_file        = self.data_file
                custom_data_filepath    = os.path.join(price_data_path,
                                                       custom_data_file)
                if int(self.verbosity) > 1:
                    print("Using data file specified ({}).".format(custom_data_file))
                data            = pd.read_csv(custom_data_filepath, 
                                              index_col = 0)
                data.index = pd.to_datetime(data.index)
                quote_data = data
                
            else:
                if int(self.verbosity) > 1:
                    print("\nDownloading OHLC price data for {}.".format(instrument))
                
                if self.optimise_mode is True:
                    # Check if historical data already exists
                    historical_data_name = 'hist_{0}{1}.csv'.format(interval, instrument)
                    historical_quote_data_name = 'hist_{0}{1}_quote.csv'.format(interval, instrument)
                    data_dir_path = os.path.join(self.home_dir, 'price_data')
                    historical_data_file_path = os.path.join(self.home_dir, 
                                                             'price_data',
                                                             historical_data_name)
                    historical_quote_data_file_path = os.path.join(self.home_dir, 
                                                             'price_data',
                                                             historical_quote_data_name)
                    
                    if not os.path.exists(historical_data_file_path):
                        # Data file does not yet exist
                        data        = getattr(self.get_data, feed.lower())(instrument,
                                                         granularity = interval,
                                                         start_time = from_date,
                                                         end_time = to_date)
                        quote_data  = getattr(self.get_data, feed.lower() + '_quote_data')(data,
                                                                                      instrument,
                                                                                      interval,
                                                                                      from_date,
                                                                                      to_date)
                        data, quote_data    = self.broker_utils.check_dataframes(data, quote_data)
                        
                        # Check if price_data folder exists
                        if not os.path.exists(data_dir_path):
                            # If price data directory doesn't exist, make it
                            os.makedirs(data_dir_path)
                            
                        # Save data in file/s
                        data.to_csv(historical_data_file_path)
                        quote_data.to_csv(historical_quote_data_file_path)
                        
                    else:
                        # Data file does exist, import it as dataframe
                        data = pd.read_csv(historical_data_file_path, 
                                           index_col = 0)
                        quote_data = pd.read_csv(historical_quote_data_file_path, 
                                                 index_col = 0)
                        
                else:
                    data        = getattr(self.get_data, feed.lower())(instrument,
                                                         granularity = interval,
                                                         start_time = from_date,
                                                         end_time = to_date)
                    quote_data  = getattr(self.get_data, feed.lower() + '_quote_data')(data,
                                                                    instrument,
                                                                    interval,
                                                                    from_date,
                                                                    to_date)
                    
                    data, quote_data    = self.broker_utils.check_dataframes(data, quote_data)
                
                
                if int(self.verbosity) > 1:
                    print("  Done.\n")
            
            return data, quote_data
            
        else:
            # Running in livetrade mode or scan mode
            data = getattr(self.get_data, feed.lower())(instrument,
                                                         granularity = interval,
                                                         count=period)
            if self.check_data_alignment:
                data = self._verify_data_alignment(data, instrument, feed, period, 
                                                  price_data_path)
        
            return data, None


    def _verify_data_alignment(self, data, instrument, feed, period, price_data_path):
        '''
        Verifies data time-alignment based on current time and last
        candle in data.
        '''
        interval = self.strategy_params['granularity']
        
        # Check data time alignment
        current_time        = datetime.now(tz=pytz.utc)
        last_candle_closed  = self.broker_utils.last_period(current_time, interval)
        data_ts             = data.index[-1].to_pydatetime().timestamp()
        
        if data_ts != last_candle_closed.timestamp():
            # Time misalignment detected - attempt to correct
            count = 0
            while data_ts != last_candle_closed.timestamp():
                print("  Time misalginment detected at {}".format(datetime.now().strftime("%H:%M:%S")),
                      "({}/{}).".format(data.index[-1].minute, last_candle_closed.minute),
                      "Trying again...")
                time.sleep(3) # wait 3 seconds...
                data    = getattr(self.get_data, feed.lower())(instrument,
                                    granularity = interval,
                                    count=period)
                data_ts = data.index[-1].to_pydatetime().timestamp()
                count   += 1
                if count == 3:
                    break
            
            if data_ts != last_candle_closed.timestamp():
                # Time misalignment still present - attempt to correct
                # Check price data directory to see if the stream has caught 
                # the latest candle
                price_data_filename = "{0}{1}.txt".format(interval, instrument)
                abs_price_path      = os.path.join(price_data_path, price_data_filename)
                
                if os.path.exists(abs_price_path):
                    # Price data file matching instrument and granularity 
                    # exists, check latest candle in file
                    f                   = open(abs_price_path, "r")
                    price_lines         = f.readlines()
                    
                    if len(price_lines) > 1:
                        latest_candle       = price_lines[-1].split(',')
                        latest_candle_time  = datetime.strptime(latest_candle[0],
                                                                '%Y-%m-%d %H:%M:%S')
                        UTC_last_candle_in_file = latest_candle_time.replace(tzinfo=pytz.UTC)
                        price_data_ts       = UTC_last_candle_in_file.timestamp()
                        
                        if price_data_ts == last_candle_closed.timestamp():
                            data    = self.broker_utils.update_data_with_candle(data, latest_candle)
                            data_ts = data.index[-1].to_pydatetime().timestamp()
                            print("  Data updated using price stream.")
            
            # if data is still misaligned, perform manual adjustment.
            if data_ts != last_candle_closed.timestamp():
                print("  Could not retrieve updated data. Aborting.")
                sys.exit(0)
        
        return data
    
    
    def _update(self, i):
        '''
        Update strategy with latest data and generate latest signal.
        '''
        
        # First clear self.latest_orders
        self.latest_orders = []
        
        open_positions      = self.broker.get_open_positions(self.instrument)
        
        # Run strategy to get signals
        signal_dict = self.strategy.generate_signal(i, open_positions)
        
        if 0 not in signal_dict:
            # Single order signal, nest in dictionary to allow iteration
            signal_dict = {1: signal_dict}
            
        # Begin iteration over signal_dict to extract each order
        for order in signal_dict:
            order_signal_dict = signal_dict[order].copy()
            
            if order_signal_dict["direction"] != 0:
                self._process_signal(order_signal_dict, i, self.data, 
                                    self.quote_data, self.instrument)
        
        if int(self.verbosity) > 1:
            if len(self.latest_orders) > 0:
                for order in self.latest_orders:
                    order_string = "{}: {} {}".format(order['order_time'], 
                                                      order['instrument'], 
                                                      order['order_type']) + \
                        " order of {} units placed at {}.".format(order['size'],
                                                                  order['order_price'])
                    print(order_string)
            else:
                print("No signal detected.")
        
        # Check for orders placed and/or scan hits
        if int(self.notify) > 0 and self.backtest_mode is False:
            
            for order_details in self.latest_orders:
                self.broker_utils.write_to_order_summary(order_details, 
                                                         self.order_summary_fp)
            
            if int(self.notify) > 1 and \
                self.email_params['mailing_list'] is not None and \
                self.email_params['host_email'] is not None:
                    if int(self.verbosity) > 0 and len(self.latest_orders) > 0:
                            print("Sending emails ...")
                            
                    for order_details in self.latest_orders:
                        emailing.send_order(order_details,
                                            self.email_params['mailing_list'],
                                            self.email_params['host_email'])
                        
                    if int(self.verbosity) > 0 and len(self.latest_orders) > 0:
                            print("  Done.\n")
            
        # Check scan results
        if self.scan_mode:
            # Construct scan details dict
            scan_details    = {'index'      : self.scan_index,
                               'strategy'   : self.strategy.name,
                               'timeframe'  : self.strategy_params['granularity']
                                }
            
            # Report AutoScan results
            # Scan reporting with no emailing requested.
            if int(self.verbosity) > 0 or \
                int(self.notify) == 0:
                if len(self.scan_results) == 0:
                    print("No hits detected.")
                else:
                    print(self.scan_results)
            
            if int(self.notify) > 0:
                # Emailing requested
                if len(self.scan_results) > 0 and \
                    self.email_params['mailing_list'] is not None and \
                    self.email_params['host_email'] is not None:
                    # There was a scanner hit and email information is provided
                    emailing.send_scan_results(self.scan_results, 
                                                scan_details, 
                                                self.email_params['mailing_list'],
                                                self.email_params['host_email'])
                elif int(self.notify) > 1 and \
                    self.email_params['mailing_list'] is not None and \
                    self.email_params['host_email'] is not None:
                    # There was no scan hit, but notify set > 1, so send email
                    # regardless.
                    emailing.send_scan_results(self.scan_results, 
                                                scan_details, 
                                                self.email_params['mailing_list'],
                                                self.email_params['host_email'])
                    
    
    def _update_backtest(self, i):
        '''
        Updates virtual broker with latest price data.
        '''
        candle = self.data.iloc[i]
        self.broker.update_positions(candle, self.instrument)
    
    
    def _process_signal(self, order_signal_dict, i, data, quote_data, 
                       instrument):
        '''
            Process order_signal_dict and send orders to broker.
        '''
        signal = order_signal_dict["direction"]
        
        # Entry signal detected, get price data
        price_data      = self.broker.get_price(instrument=instrument, 
                                                data=data, 
                                                conversion_data=quote_data, 
                                                i=i)
        datetime_stamp  = data.index[i]
        
        if signal < 0:
            order_price = price_data['bid']
            HCF         = price_data['negativeHCF']
        else:
            order_price = price_data['ask']
            HCF         = price_data['positiveHCF']
        
        
        # Define 'working_price' to calculate size and TP
        if order_signal_dict["order_type"] == 'limit' or order_signal_dict["order_type"] == 'stop-limit':
            working_price = order_signal_dict["order_limit_price"]
        else:
            working_price = order_price
        
        # Calculate exit levels
        pip_value   = self.broker_utils.get_pip_ratio(instrument)
        stop_distance = order_signal_dict['stop_distance'] if 'stop_distance' in order_signal_dict else None
        stop_type = order_signal_dict['stop_type'] if 'stop_type' in order_signal_dict else None
        
        if 'stop_loss' not in order_signal_dict and \
            'stop_distance' in order_signal_dict and \
            order_signal_dict['stop_distance'] is not None:
            stop_price = working_price - np.sign(signal)*stop_distance*pip_value
        else:
            stop_price = order_signal_dict['stop_loss'] if 'stop_loss' in order_signal_dict else None
        
        if 'take_profit' not in order_signal_dict and \
            'take_distance' in order_signal_dict and \
            order_signal_dict['take_distance'] is not None:
            # Take profit distance specified
            take_profit = working_price + np.sign(signal)*order_signal_dict['take_distance']*pip_value
        else:
            # Take profit price specified, or no take profit specified at all
            take_profit = order_signal_dict["take_profit"] if 'take_profit' in order_signal_dict else None
        
        # Calculate risked amount
        amount_risked = self.broker.get_balance() * self.strategy_params['risk_pc'] / 100
        
        # Calculate size
        if 'size' in order_signal_dict:
            size = order_signal_dict['size']
        else:
            if self.strategy_params['sizing'] == 'risk':
                size            = self.broker_utils.get_size(instrument,
                                                 amount_risked, 
                                                 working_price, 
                                                 stop_price, 
                                                 HCF,
                                                 stop_distance)
            else:
                size = self.strategy_params['sizing']
        
        # Construct order dict by building on signal_dict
        order_details                   = order_signal_dict
        order_details["order_time"]     = datetime_stamp
        order_details["strategy"]       = self.strategy.name
        order_details["instrument"]     = instrument
        order_details["size"]           = signal*size
        order_details["order_price"]    = order_price
        order_details["HCF"]            = HCF
        order_details["granularity"]    = self.strategy_params['granularity']
        order_details["stop_distance"]  = stop_distance
        order_details["stop_loss"]      = stop_price
        order_details["take_profit"]    = take_profit
        order_details["stop_type"]      = stop_type
        order_details["related_orders"] = order_signal_dict['related_orders'] if 'related_orders' in order_signal_dict else None

        # Place order
        if self.scan_mode:
            # Bot is scanning
            scan_hit = {"size"  : size,
                        "entry" : order_price,
                        "stop"  : stop_price,
                        "take"  : take_profit,
                        "signal": signal
                        }
            self.scan_results[instrument] = scan_hit
            
        else:
            # Bot is trading
            self.broker.place_order(order_details)
            self.latest_orders.append(order_details)
            
            

    def create_backtest_summary(self, balance, NAV, margin):
        '''
        Constructs backtest summary dictionary for further processing.
        '''
        
        trade_summary = self.broker_utils.trade_summary(self.instrument, self.broker.closed_positions)
        open_trade_summary = self.broker_utils.open_order_summary(self.instrument, self.broker.open_positions)
        cancelled_summary = self.broker_utils.cancelled_order_summary(self.instrument, self.broker.cancelled_orders)
        
        if self.validation_file is not None:
            livetrade_summary = self.validation_utils.trade_summary(self.raw_livetrade_summary,
                                                                    self.data,
                                                                    self.strategy_params['granularity'])
            final_balance_diff  = NAV[-1] - livetrade_summary.Balance.values[-1]
            filled_live_orders  = livetrade_summary[livetrade_summary.Transaction == 'ORDER_FILL']
            no_live_trades      = len(filled_live_orders)
            self.livetrade_results = {'summary': livetrade_summary,
                                      'final_balance_difference': final_balance_diff,
                                      'no_live_trades': no_live_trades}
            
        backtest_dict = {}
        backtest_dict['data']           = self.data
        backtest_dict['NAV']            = NAV
        backtest_dict['balance']        = balance
        backtest_dict['margin']         = margin
        backtest_dict['trade_summary']  = trade_summary
        backtest_dict['indicators']     = self.strategy.indicators if hasattr(self.strategy, 'indicators') else None
        backtest_dict['instrument']     = self.instrument
        backtest_dict['interval']       = self.strategy_params['granularity']
        backtest_dict['open_trades']    = open_trade_summary
        backtest_dict['cancelled_trades'] = cancelled_summary
        
        self.backtest_summary = backtest_dict
    
    def _get_iteration_range(self):
        '''
        Checks mode of operation and returns data iteration range. For backtesting,
        the entire dataset is iterated over. For livetrading, only the latest candle
        is used.
        '''
        
        if self.backtest_mode:
            start_range = 0
        else:
            start_range = len(self.data)-1
        end_range       = len(self.data)

        return start_range, end_range
    