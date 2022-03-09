
from __future__ import print_function

from re import split

#for using dictionary with dot notations
from types import SimpleNamespace

import socket, json, logging, threading, queue, concurrent.futures, stripe, mailersend_email,  window, tempfile, datetime

import stripe #for error handling

#Producer reads the incoming TCP requests and puts it in a in_queue for consumer to consume it.  
#Never holds the reading of TCP unless client expects a results of execution.  In that case out_queue from consumer is passed to client
def producer(in_queue, out_queue,exit_event):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0)) #this should bind to free port
        add, port = s.getsockname()
    
        # Save the connection detail for the external app to know 
        with open('connection.txt', 'w') as connFile:
            connFile.write(f"Listening Address = {add}\nListening Port = {port}")
        
        while not exit_event.is_set():
            logging.info(f"Listening On Address: {add} Port: {port}")
            s.listen()
            conn, addr = s.accept()
        
            with conn:
                print('Connected by', addr)
                while not exit_event.is_set():
                    try:
                        data = conn.recv(102400) #100kb buffer on tcp receiver
                    except (ConnectionResetError, ConnectionAbortedError) as e:
                        logging.info("Producer: Connection reset on client end")
                        break
                    except socket.error as e:
                        print(e)
                        logging.error("Error on socket",exc_info=True)
                        break #This breaks to listen TCP again discarding the old data on the receive buffer
                    if not data:
                        break
                    
                    # If data received, do the following
                    try:
                        logging.debug(f"Producer: Requet from TCP \n{data}")
                        split_data = data.splitlines() 
                        logging.debug(f"Producer: Data after splitting:\n{split_data}")
                        for data in split_data:
                            logging.debug(f"Producer: Data Being Processed is \n{data}")
                            lv_request=json.loads(data)
                            logging.debug(f"Producer: JSON loads of receved data \n{lv_request}")
                            request=SimpleNamespace(**lv_request) #Type Creation from json string. Converts a string to a function object
                            logging.info(f"Producer: Received request \n{request}\n")
                            in_queue.put(request)
                            logging.debug(f"Producer: Added request to consumer in_queue")
                            if request.return_expected:
                                out_data=out_queue.get()
                                conn.send((json.dumps(out_data)+"\r\n").encode())  #waits here until outqueue is filled from consumer after executing the statement.
                                logging.info(f"Producer: Response to TCP \n{out_data}")
                    
                    except Exception as e:
                        logging.error("Producer: Execption at producer loop",exc_info=True)


#Consumer consumes the messages from the producer and executes the messages one by one.
#outputs the result if client reuqested the results of execution.  Inthat case out_queue is used to pass results to client.
def consumer(in_queue, out_queue, exit_event):
    
    while not exit_event.is_set() or not in_queue.empty():
        request = in_queue.get()
        logging.debug(f"Consumer: Received request \n{request}\n")
        try:
            logging.debug(f"Consumer: Starts executing \n{request}\n")
            lv_response=eval(request.func + "(request.args)")
            result = {'status': True, 'info': json.dumps(lv_response)} #status True for success
            logging.debug(f"Consumer: Execution result \n{result}\n")

        except (socket.gaierror, stripe.error.APIConnectionError) as e:
            logging.exception(f"Consumer: Socket error occured on executing request.  Please check internet connection")
            result = {'status': False, 'info': "Socket error occured on executing request.  Please check internet connection"} #status False for error or failures

        except Exception as e:
            logging.exception(f"Consumer: Execption occured on executing request\n{str(request)}\n{format(e)}")
            result = {'status': False, 'info': format(e)} #status False for error or failures

        finally:
            if request.return_expected:                
                logging.debug(f"Consumer: Sending data to TCP \n{result}")
                out_queue.put(result)

def main():
    format = '%(asctime)s|%(name)s|%(levelname)s|%(message)s\n\n'
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    # create file handler which logs even debug messages
    logger = logging.getLogger()
    timestamp = datetime.datetime.now().strftime("%Y-%b-%d-%H.%M.%S")
    f = tempfile.gettempdir()+f'\\LV_GSheet_{timestamp}.log'

    logger.info(f'Logging to temporary file {f}')
    fh = logging.FileHandler(f)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)          

    pipeline_in = queue.Queue()
    pipeline_out = queue.Queue()
    exit_event = threading.Event()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(producer, pipeline_in, pipeline_out, exit_event)
        executor.submit(consumer, pipeline_in, pipeline_out, exit_event)
        executor.submit(window.user_interface, exit_event)
    '''
        time.sleep(0.1)
        logging.info("Main: about to set event")
        exit_event.set()
    '''
    

if __name__ == '__main__':
    main()