import base64
import pickle
import pprint

# 1. PASTE YOUR BASE64 _vars STRING HERE
encoded = "gASVqwAAAAAAAAB9lCiMD3NwZWVkZXJfY291bnRlcpRLJowTcGFydGljaXBhbnRzX25lZWRlZJRN3AWMF3ByZXNjcmVlbmVyX2dyb3Vwc19kaWN0lH2UKEsAfZQojAdjdXJyZW50lEtLjAttYXhfYWxsb3dlZJRN7wF1SwF9lChoBksmaAdL+XVLAn2UKGgGS4hoB0v5dUsDfZQoaAZLcmgHS/l1SwR9lChoBkuyaAdL+XV1dS4="

# 2. DECODE + UNPICKLE
binary_data = base64.b64decode(encoded)
vars_dict = pickle.loads(binary_data)

print("CURRENT CONTENT OF _vars (Python dict):\n")
pprint.pprint(vars_dict)


# 3. >>>>>>> EDIT HERE <<<<<<
# After you run once and see the dict, come back here and change values.

# Examples – CHANGE OR DELETE ACCORDING TO WHAT YOU NEED:
# vars_dict["participants_needed"] = 10
# vars_dict["speeder_counter"] = 0
vars_dict["prescreener_groups_dict"][0]["current"] = 75
vars_dict["prescreener_groups_dict"][1]["current"] = 38
vars_dict["prescreener_groups_dict"][2]["current"] = 136
vars_dict["prescreener_groups_dict"][3]["current"] = 113
vars_dict["prescreener_groups_dict"][4]["current"] = 178

# 4. RE-PICKLE + BASE64-ENCODE
new_binary = pickle.dumps(vars_dict, protocol=pickle.HIGHEST_PROTOCOL)
new_encoded = base64.b64encode(new_binary).decode("ascii")

print("\nNEW BASE64 _vars STRING (paste this into the database):\n")
print(new_encoded)