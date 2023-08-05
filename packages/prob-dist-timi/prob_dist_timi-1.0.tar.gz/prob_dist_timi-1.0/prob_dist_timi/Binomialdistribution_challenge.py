import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
                
    """
    
    #       A binomial distribution is defined by two variables: 
    #           the probability of getting a positive outcome
    #           the number of trials
    
    #       If you know these two values, you can calculate the mean and the standard deviation
    #       
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))
    
    #       

    def __init__(self, prob = 0.5, size = 20):
        
        # TODO: store the probability of the distribution in an instance variable p
        self.p = prob
        # TODO: store the size of the distribution in an instance variable n
        self.n = size
        
        # TODO: Now that you know p and n, you can calculate the mean and standard deviation
        #       You can use the calculate_mean() and calculate_stdev() methods defined below along with the __init__ function from the Distribution class
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        self.mean = self.n * self.p

        return self.mean

    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))

        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
        self.n = len(self.data)
        self.p = 1.0 * (sum(self.data) / len(self.data))
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n
    
    
    def plot_bar(self)
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        plt.hist(x = [0, 1], height = [(1 - self.p) * self.n, self.p * self.n])
        plt.title('Bar Chart of Data Set')
        plt.xlabel('Outcome')
        plt.ylabel('Count')
    
    
    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        a = math.factorial(self.n) / ((math.factorial(k)) * (math.factorial(self.n - k)))
        b = self.p ** k * ((1 - self.p) ** (self.n - k))

    
    def plot_pdf(self):
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
    
        x = []
        y = []

        for i in range(self.n + 1):
            x = append(i)
            y = append(pdf(i))

        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.xlabel('Probability')
        plt.ylabel('Outcome')

        plt.show()
        return x, y
                
    
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.n = self.n + other.n
        result.p = self.px
        result.calculate_mean()
        result.calculate_stdev()
                        

    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """
    
        return "mean {0}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
