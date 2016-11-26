import sys
import GetInfectedIPs
import ProcessLogs

if __name__ == "__main__":
    # 0. argument is name of the file
    # 1. argument is path to the dataset

    # Terminate it if no these argument !!!!!!!!
    if len(sys.argv) > 1:
        path = sys.argv[1]

    path = 'C:\\Users\\frenk\\Documents\\Skola\\Stratosphere\\datasets\\CTU-13-Dataset.tar\\1'

    # 1. Get infected IpAddress from labeled binetflow
    # Infected_ips has two components:
    # a. infected_ips[0] = infected_ips_list is array of infected ipAddresses
    # b. infected_ips[1] = infected_ips is dictionary,where index is ipAdrress and value is number of infected ipAddress
    infected_ips = GetInfectedIPs.get_infected_ips(path)

    # 2. Create 4-tuples, evaluate features and labeled them
    process_logs = ProcessLogs.ProcessLog(path, infected_ips[0])
    process_logs.evaluate_features()
    # process_logs.print_connection_4_tuple()
    process_logs.check_4_tuples()
