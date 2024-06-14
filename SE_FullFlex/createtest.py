import csv
import Solvefile as Sf
import pandas as pd
from openpyxl import Workbook


def write_data_test(numslices_list : list,
                    allconfig_list : list,
                    filename):
    """
    Writes data to a CSV file.

    Args:
        data: A list of lists representing the data to be written.
        filename: The filename for the output CSV file (default: "output.csv").
    """
    # Open the CSV file in write mode
    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        for numslices in numslices_list:
            for config_list in allconfig_list:
                accept_slices, runtime, rate = Sf.SolveSE_FullFelx(numslices=numslices,config_list=config_list)
                accept_rate = accept_slices/numslices
                # Write the data to the CSV file
                writer.writerow([str(numslices),
                                config_list,
                                accept_slices,
                                accept_rate,
                                runtime,
                                rate
                                ])
                
        

write_data_test(numslices_list=[10,15],
                allconfig_list=[['C1'],['C3'],['C1','C3']],
                filename="./testresult/testresult_per5_1.csv")
       
    
    
    