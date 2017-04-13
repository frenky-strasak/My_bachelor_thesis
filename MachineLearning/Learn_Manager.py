import Get_normalize_data
import SVM

path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/My_bachelor_thesis/MachineLearning/Data_Connection/conn_result.txt"

norm_train_data, train_labels, norm_test_data, test_labels = Get_normalize_data.main(path)

SVM.detect(norm_train_data, train_labels, norm_test_data, test_labels)