from createtest import write_data_test

def main():
    # Simply write the result in csv file
    write_data_test(numslices_list=[20],
                allconfig_list=[['k1'],['k2'],['k1','k2']],
                phyname_list=["Abilene","Atlanta","Polska"],
                filename="./testresult/testresult_per5_20.csv")
    
if __name__ == "__main__":
    main()