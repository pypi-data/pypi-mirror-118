import matplotlib.pyplot as plt
import math

class VisualizationCode:
    def __init__(self):
        """
        Class to create different well labelled visualizations such as line plots, and bar charts based off matplotlib
        
        """
        
        x = []
        y = []
        
    def data(data_1, data_2):
        """Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute.
				
		Args:
			data_1 and data_2 (string): names of files to read from
		
		Returns:
			x and y: data read from data_1 and data_2 respectively
		
		"""
        with open(data_1, data_2) as file1, file2:
            data_1_list = []
            line1 = file1.readline()
            while line1:
                data_1_list.append(int(line1))
                line1 = file.readline()
                
            data_2_list = []
            line1 = file2.readline()
            while line2:
                data_2_list.append(int(line2))
                line2 = file.readline()
       data_1.close()
       data_2.close()
        
       x = data_1_list
       y = data_2_list
        
       return x, y
    
    def plot_line(x,y):
        #FUNCTION TO PLOT THE LINE PLOT 
        plt.figure(figsize =(7,4))
        plt.plot(x, y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        plt.title('Line Plot showing the relationship between x and y', fontsize = 15)
        plt.ylabel('y', fontsize = 11)
        plt.xlabel('x', fontsize = 11)
        plt.grid(True)
        plt.show()
        

        
    def plot_bar(x,y):
        #FUNCTION TO PLOT THE BAR PLOT 

        plt.bar(x, y, color='red', marker='o', linestyle='dashed', linewidth=2, markersize=12)
        plt.title('Distribution of Data', fontsize = 15)
        plt.ylabel('y', fontsize = 11)
        plt.xlabel('x', fontsize = 11)

        plt.show()