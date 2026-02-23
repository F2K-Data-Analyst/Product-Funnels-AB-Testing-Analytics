#%%
import pandas as pd
# %%
# Load Datasets 
Users = pd.read_csv(r"C:\Users\Fseha\OneDrive\Desktop\Fish documents\school documents\Data Analysis docs\Full  EDA projects\Python Project\data\Raw\users.csv")
Sessions = pd.read_csv(r"C:\Users\Fseha\OneDrive\Desktop\Fish documents\school documents\Data Analysis docs\Full  EDA projects\Python Project\data\Raw\sessions.csv")
Purchases = pd.read_csv(r"C:\Users\Fseha\OneDrive\Desktop\Fish documents\school documents\Data Analysis docs\Full  EDA projects\Python Project\data\Raw\purchases.csv")
Experiments = pd.read_csv(r"C:\Users\Fseha\OneDrive\Desktop\Fish documents\school documents\Data Analysis docs\Full  EDA projects\Python Project\data\Raw\experiments.csv")
Experiments_Assignments = pd.read_csv(r"C:\Users\Fseha\OneDrive\Desktop\Fish documents\school documents\Data Analysis docs\Full  EDA projects\Python Project\data\Raw\experiment_assignments.csv")

print("Users Shape:", Users.shape)
print("Sessions Shape:", Sessions.shape)
print("Purchases Shape:", Purchases.shape)

Users.head()
# %%
