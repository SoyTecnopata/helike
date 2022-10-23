import pandas as pd
import numpy as np

df = pd.read_csv("inputs.csv")

df["edad"] = int(2022) - df["c_year"]

# Segmentacion por edades


# Canal Chatbot
df["Canal"] = np.where( df["edad"] > 0 & df["edad"] <= 35,
                        "Chat-bot",
                        "Otros Canales" 
                          )

# Canal Contact Center
df["Canal"] = np.where( df["edad"] > 35 & df["edad"] <= 45,
                        "Contact Center",
                        "Otros Canales" 
                          )

# Canal E-Mail
df["Canal"] = np.where( df["edad"] > 45 & df["edad"] <= 60,
                        "Contact Center",
                        "Otros Canales" 
                          )

# Canal E-Mail
df["Canal"] = np.where( df["edad"] > 60 & df["edad"] <= 80,
                        "Contact Center",
                        "Otros Canales" 
                          )