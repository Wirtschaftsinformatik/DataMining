#from tkinter import Tk,Label,IntVar,Checkbutton,Button,mainloop,W,Entry
#from tkinter.messagebox import ans
import tkinter as tk
from tkinter.font import Font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from eda import eda


def show_answer():
    # clear old output
    Output_Box_One.delete(1.0, "end")
    Output_Box_Two.delete(1.0, "end")
    Output_Box_Three.delete(1.0, "end")
    # get the radio button selection / wich option got selected
    radio_get = radio.get()

    # catch 0 option selection
    if radio_get == 0:
        Output_Box_Three.insert("end", "No checkboxes are enabled" +"\n" + "select at least one")
    
    # Option 1
    # get the Parameters from the entry boxes
    # parse to int so they can be used for the function call in eda.py
    # check boxes for laplace and bitvector
    # will maybe change to radio button "soon^tm"
    # call output function with return values
    elif radio_get == 1:
        num_weights = int(input_chromosom.get())
        solutions = int(input_solutions.get())
        num_parents = int(input_parents.get())
        generations = int(input_generations.get())
        if list(laplace_bar.state()) == [0,0]:
            laplace_box = 1
        elif list(laplace_bar.state()) == [1,0]:
            laplace_box = 1 
        elif list(laplace_bar.state()) == [0,1]:
            laplace_box = 0
        if list(bitvector_bar.state()) == [0,0]:
            bit = 1
        elif list(bitvector_bar.state()) == [1,0]:
            bit = 1 
        elif list(bitvector_bar.state()) == [0,1]:
            bit = 0
        titel = "Random with self defined Parameters"         
        return_simulation = eda.eda_random(num_weights, solutions, num_parents, generations, laplace_box, bit, titel)
        button_output(return_simulation, generations, titel)
    # Option 2
    # check boxes for laplace and bitvector
    # will maybe change to radio button "soon^tm"
    # call output function with return values from random with laplace 0/1 and bitvector 0/1
    elif radio_get == 2:
        if  (list(bitvector_bar.state())) == [0,0]:
            loop_range = 4
            return_simulation = eda.eda_random(8, 10, 3, 4, 1, 1, "Random with fixed Parameters")
            button_output(return_simulation, loop_range, "Random with fixed Parameters")
        elif (list(bitvector_bar.state())) == [1,0]:
            loop_range = 4
            return_simulation = eda.eda_random(8, 10, 3, 4, 1, 1, "Random with fixed Parameters")
            button_output(return_simulation, loop_range, "Random with fixed Parameters")
        elif (list(bitvector_bar.state())) == [0,1]:
            loop_range = 4
            return_simulation = eda.eda_random(8, 10, 3, 4, 1, 0, "Random with fixed Parameters")
            button_output(return_simulation, loop_range, "Random with fixed Parameters")
    # Option 3
    # call output function with return values from fixed without laplace
    elif radio_get == 3:
        loop_range = 6
        return_simulation = eda.eda_fixed(0, "Short Example without Laplace")
        button_output(return_simulation, loop_range, "Short Example without Laplace")
    # Option 4
    # call output function with return values for fixed with laplace
    elif radio_get == 4:
        loop_range = 6
        return_simulation = eda.eda_fixed(1, "Short Example with Laplace-Correction")
        button_output(return_simulation, loop_range, "Short Example with Laplace-Correction")
                
def button_output(return_simulation, loop_range, titel):
    # Extract values from the return string
    # return string is a list 
    # [new_pop, [generation, parents, probability_model, best_gen_fitness]^for_each_generation, target_fitness, plot_fitness, best_fitness_found]
    # new_pop: starting Population
    #   generation: number of current generation -> followed by 3 values for that generation
    #   parents: chromosomes that have the best fitness this generation
    #   probability_model: probability vector for this generation
    #   best_gen_fitness: best fitness found in this generation
    #   gen_pop: population for this generation
    # target_fitness: best possible fitness
    # plot_fitness: numpy array containing all fitness values of each generation for plotting
    # best_fitness_found: best overrall achieved fitness
    new_pop = return_simulation [0]
    generation_all = return_simulation[1]

    target_fitness = return_simulation [2]
    solutions = return_simulation [3]
    plot_fitness = return_simulation [4]
    best_fitness_found = return_simulation[5]

    # output starting generation to Box1
    Output_Box_One.insert("end", new_pop)
    # setting x value for plot
    x = []
    # output of the inner list with values for each generation to box 2
    for i in range(loop_range):
        generation = return_simulation[1][i][0]
        parents = return_simulation[1][i][1]
        prob_model = return_simulation[1][i][2]
        best_gen_fitness = return_simulation[1][i][3]
        Output_Box_Two.insert("end", "Generation: " + str(generation) + "\n")
        Output_Box_Two.insert("end", "Parents selected for mating: " + "\n" + str(parents) + "\n")
        Output_Box_Two.insert("end", "Generated Probability Model: " + "\n" + str(prob_model) + "\n")
        Output_Box_Two.insert("end", "Best Fitness this Generation: " + str(best_gen_fitness) + "\n")
        Output_Box_Two.insert("end", "\n")
        x.append(i+1)

    # output of final values to Box 3
    Output_Box_Three.insert("end", "Ergebnisse" +"\n")
    Output_Box_Three.insert("end", "Target Fitness: " + str(target_fitness) +"\n")
    Output_Box_Three.insert("end", "Best Fitness found: " + str(best_fitness_found) +"\n")
    Output_Box_Three.insert("end", "Best Solution(s)" + str(solutions)  +"\n")

    # output the plot 
    # generating new widged containing the plot
    # plotting x(number generations) and the numpy array with all fitness values
    # setting titel and label
    output_plot = plt.Figure(figsize=(5,4), dpi=100)
    ax = output_plot.add_subplot(111)
    ax.plot(x, plot_fitness)
    line = FigureCanvasTkAgg(output_plot, master)
    line.get_tk_widget().grid(row=15)
    ax.set_title(titel)
    ax.set_xlabel('Generation')
    ax.set_ylabel('Fitness')

    toolbarFrame = tk.Frame(master)
    toolbarFrame.grid(row=25)
    toolbar = NavigationToolbar2Tk(line, toolbarFrame)

# custom class with checkbars next to each other 
# will probably have to be changed into radioboxes
# have to look into setting the value parameter for radioboxes properly
class Checkbar(tk.Frame):
   def __init__(self, parent=None, picks=[], side=tk.LEFT, anchor=tk.W):
      tk.Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = tk.IntVar()
         chk = tk.Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=1)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)
if __name__ == "__main__":

    master = tk.Tk()
    text = tk.Text(master)
    myFont = Font(family="Times New Roman", size = 12)
    text.configure(font=myFont)

    # starting Labels 
    tk.Label(master, text="Welcome to a small eda example").grid(row=0)
    tk.Label(master, text="You have the following Options: :").grid(row=1, sticky=tk.W)

    # radiobuttons for the 4 different Options
    radio = tk.IntVar()
    tk.Radiobutton(master, text="-- [1] Define the parameters that get run for a random generated bitvector", 
                    variable=radio, value=1).grid(row=2, sticky=tk.W)
    tk.Radiobutton(master, text="-- [2] A pre difined example run with random generated bitvectors || Optional bitvector Parameter", 
                    variable=radio, value=2).grid(row=3, sticky=tk.W)
    tk.Radiobutton(master, text="-- [3] Run an example showing the eda-algorithm as per the lecture, without Laplace Correction", 
                    variable=radio, value=3).grid(row=4, sticky=tk.W)
    tk.Radiobutton(master, text="-- [4] Run an example showing the eda-algorithm as per the lecture, with Laplace-Correction", 
                    variable=radio, value=4).grid(row=5, sticky=tk.W)

    # formatting
    tk.Label(master, text="").grid(row=6, sticky=tk.W)
    tk.Label(master, text="Input Parameters for Option 1: :").grid(row=7, sticky=tk.W)

    # label + input fields for Parameters for Option 1
    tk.Label(master, text="Number of Chromosom:").grid(row=8, sticky=tk.W)
    input_chromosom = tk.Entry(master)
    input_chromosom.grid(row=8)

    tk.Label(master, text="Number of Solutions:").grid(row=9, sticky=tk.W)
    input_solutions = tk.Entry(master)
    input_solutions.grid(row=9)

    tk.Label(master, text="Number of Parents for mating:").grid(row=10, sticky=tk.W)
    input_parents = tk.Entry(master)
    input_parents.grid(row=10)

    tk.Label(master, text="Number of Generations:").grid(row=11, sticky=tk.W)
    input_generations = tk.Entry(master)
    input_generations.grid(row=11)

    # Label + custom checkboxes for the Laplace and bitvector selection
    tk.Label(master, text="Laplace Correction:").grid(row=12, sticky=tk.W)
    laplace_bar = Checkbar(master, ["Ja","Nein"])
    laplace_bar.grid(row=12)

    tk.Label(master, text="Bitvector (0 or 1) or full range (0-1) vector:").grid(row=13, sticky=tk.W)
    bitvector_bar = Checkbar(master, ["bitvector","full range"])
    bitvector_bar.grid(row=13)

    # more formatting
    tk.Label(master, text="     ").grid(row=14, sticky=tk.W)
    tk.Label(master, text="              ").grid(row=14, column=2 , sticky=tk.W)

    # setting output boxes to column 2 so the space on the right side of the gui can be used
    Output_Box_One = tk.Text(master, height = 2, width = 50, font= myFont)
    Output_Box_One.grid(row=1, column=3, rowspan=5, columnspan = 2, sticky = tk.W+tk.E+tk.N+tk.S)

    Output_Box_Two = tk.Text(master, height = 2, width = 50, font= myFont)
    Output_Box_Two.grid(row=7, column=3, rowspan=7, columnspan = 2, sticky = tk.W+tk.E+tk.N+tk.S)

    Output_Box_Three = tk.Text(master, height = 2, width = 50, font= myFont)
    Output_Box_Three.grid(row=15, column=3, rowspan=4, columnspan = 2, sticky = tk.W+tk.E+tk.N+tk.S)
    
    # Buttons for starting the calculation and exiting the "program"
    tk.Button(master, text='Start Calculation', command=show_answer).grid(row=30, sticky=tk.W, pady=4)
    tk.Button(master, text='Quit', command=master.quit).grid(row=30, column=6, sticky=tk.E, pady=4)

    tk.mainloop()