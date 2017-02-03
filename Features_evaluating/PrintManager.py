"""
This class just print texts.
"""

from time import time


class PrintManager:
    def __init__(self):
        self.index_of_folder = 1
        self.t0 = None
        self.t1 = None
        # spaces
        self.space_1 = "     "
        self.space_2 = "         "

    # ---------------- Main_single ------------
    def welcome_main_single(self):
        print "\n" \
          "<<< Welcome to Features evaluating project !!!\n" +\
          "<<< You run Main_single.py which extracts data from single dataset.\n" \
          "<<< For more info see README.md or https://github.com/frenky-strasak/My_bachelor_thesis\n"

    def header_main_single(self, path, name_of_file):
        print "<<<-------------------------------------------------------------------\n" \
          "<<< Program will start evaluate your single dataset:\n" \
          "<<< '", path, "'\n" \
          "<<< It will crete these data files:\n" \
          "<<<          1. '" + name_of_file + "'\n" \
          "<<<-------------------------------------------------------------------"
        self.t0 = time()

    def set_finish_time(self):
        self.t1 = time()

    def succ_main_single(self):
        print "\n" \
          "<<< Successfully finished in aproximate time: %f" % (self.t1-self.t0) + " sec."

    # -------------- Main_multi -----------------------------
    def welcome_main_multi(self):
        print "\n" \
          "<<< Welcome to Features evaluating project !!!\n" +\
          "<<< You run Main_multi.py which extracts data from multi dataset.\n" \
          "<<< For more info see README.md or https://github.com/frenky-strasak/My_bachelor_thesis\n"

    def header_main_multi(self, path, size_of_len, name_of_file):
        print "<<<-------------------------------------------------------------------\n" \
          "<<< Program will start evaluate your multi dataset folder:\n" \
          "<<< '", path, "'\n" \
          "<<< Number of single data sets in multi folder: ", size_of_len, "\n" \
          "<<< It will crete these data files:\n" \
          "<<<          1. '" + name_of_file + "'\n" \
          "<<<-------------------------------------------------------------------\n"

    def header_of_single_dataset(self, path_to_single):
        print "<<<-------------------------------------------------------------------\n" \
              "<<< #" + str(self.index_of_folder) + " dataset\n" \
              "<<< '", path_to_single, "'\n" \
              "<<<-------------------------------------------------------------------"
        self.t0 = time()
        self.index_of_folder += 1

    def succ_finished_single_data(self):
        self.t1 = time()
        print "<<< This single dataset successfully finished in aproximate time: %f" % (self.t1-self.t0) + " sec"

    # ---------------- EvaluateData ---------------------------------------
    def evaluate_creating_plot(self):
        print self.space_1 + "<< Evaluate.py: Creating plot data..."

    def evaluate_creating_succ(self):
        print self.space_2 + "<< Evaluate.py: Plot data were succesfly created."

    # -------------- ProcessLog -------------------------------------------
    def processLog_evaluating(self):
        print self.space_1 + "<< ProcessLog.py: Evaluating of conn file..."

    def processLog_evaluating2(self, malware, normal, background_and_no_label, number_of_tuples, normal_tuples, malware_tuples, number_of_lines, number_adding_ssl, number_of_adding_x509):
        print self.space_2 + "<<It was read:"
        print self.space_2 + "<< ProcessLog.py: Number of lines:", number_of_lines
        print self.space_2 + "<< ProcessLog.py: Flows together:", background_and_no_label + malware + normal
        print self.space_2 + "<< ProcessLog.py: Malwares flows:", malware
        print self.space_2 + "<< ProcessLog.py: Normal flows:", normal
        print self.space_2 + "<< ProcessLog.py: Background flows:", background_and_no_label
        print self.space_2 + "<< ProcessLog.py: Number of 4-tuples:", number_of_tuples
        print self.space_2 + "<< ProcessLog.py: Normal 4-tuples:", normal_tuples
        print self.space_2 + "<< ProcessLog.py: Malware 4-tuples:", malware_tuples
        print self.space_2 + "<< ProcessLog.py: Number of added ssl logs:", number_adding_ssl
        print self.space_2 + "<< ProcessLog.py: Number of added x509 logs:", number_of_adding_x509

    def processLog_evaluate_ssl(self):
        print self.space_1 + "<< ProcessLogs.py: Evaluating of ssl file..."

    def processLog_no_ssl_logs(self):
        print self.space_2 +"<< ProcessLogs.py: This data set does not have ssl logs."

    def processLog_number_of_addes_ssl(self, count_lines):
        print self.space_2 + "<< ProcessLogs.py: Pocet radku v ssl.log: ", count_lines

    def processLog_number_of_addes_x509(self, count_lines):
        print self.space_2 + "<< ProcessLogs.py: Pocet radku v x509.log: ", count_lines

    def processLog_check_tuples(self):
        print self.space_1 + "<< ProcessLogs.py: Checking connections..."

    def processLog_result_1_of_check(self):
        print self.space_2 + "<< ProcessLog.py: Connections are ok. Each connection has 0 malwares or 0 normal."

    def processLog_result_number_of_flows(self, normal, malware):
        print self.space_2 + "<< ProcessLog.py: Total numbers of used flows is: malware:", malware, "normal:", normal
        print self.space_2 + "<< ProcessLog.py: Total numbers of used flows in our entire dataset: malware: 338468, normal: 343113"

    def processLog_result_2_of_check(self):
        print self.space_2 + "<< ProcessLog.py: CAUTION: There are some connection having malware and normal flows !!!"

    # ------------------- GetInfected IPS ------------------
    def getinfectedips_getting(self):
        print self.space_1 + "<< DetInfectedIPs.py: Getting infected IPs from binetflow."

    def getinfectedips_error1(self):
         print "Error: In current folder there is no *.binetflow or there are more binetflows.\n" \
              "Check your path to binetflow and check if there is just one binetflow file in that folder."

    def getinfectedips_error2(self):
        print "Error: There has to be a path to folder as argument, where a binetflow file is."


__PrintManager__ = PrintManager()
