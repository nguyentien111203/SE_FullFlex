import csv
import Solvefile as Sf
import pandas as pd
from openpyxl import Workbook


def write_data_test(numslices_list : list,
                    allconfig_list : list,
                    phyname_list : list,
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
                for phyname in phyname_list:
                    accept_slices,objvalue, runtime, rate, phyname = Sf.SolveSE_FullFelx(numslices=numslices,config_list=config_list,phyname=phyname)
                    accept_rate = accept_slices/numslices
                    # Write the data to the CSV file
                    writer.writerow([str(numslices),
                                objvalue,
                                config_list,
                                accept_slices,
                                accept_rate,
                                runtime,
                                rate,
                                phyname
                                ])
                
        

write_data_test(numslices_list=[20],
                allconfig_list=[['k1'],['k2'],['k1','k2']],
                phyname_list=["Abilene","Atlanta","Polska"],
                filename="./testresult/testresult_per5_20.csv")
    
    
    
    