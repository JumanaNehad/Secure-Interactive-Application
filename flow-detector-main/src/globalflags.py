stop_flag = True
modelpath = 'C:/Users/anoor/Desktop/SIA/flow-detector-main/ddos_detector_model.h5'
logopath = 'C:/Users/anoor/Desktop/SIA/flow-detector-main/logos.png'
logopathon = 'https://cdn.freebiesupply.com/logos/large/2x/sia-2-logo-png-transparent.png'
tasks = []
predictddos = True
data_file_path = 'C:/Users/anoor/Desktop/SIA/flow-detector-main/Filtered Dataset.csv'

blockedsign = """
██████  ██       ██████   ██████ ██   ██ ███████ ██████  
██   ██ ██      ██    ██ ██      ██  ██  ██      ██   ██ 
██████  ██      ██    ██ ██      █████   █████   ██   ██ 
██   ██ ██      ██    ██ ██      ██  ██  ██      ██   ██ 
██████  ███████  ██████   ██████ ██   ██ ███████ ██████                                                                                                                                                                                     

"""


emblem = """
# MMMMMMMM               MMMMMMMMIIIIIIIIIUUUUUUUU     UUUUUUU
# M:::::::M             M:::::::MI::::::::IU::::::U     U::::::U
# M::::::::M           M::::::::MI::::::::IU::::::U     U::::::U
# M:::::::::M         M:::::::::MII::::::IIUU:::::U     U:::::UU
# M::::::::::M       M::::::::::M  I::::I   U:::::U     U:::::U 
# M:::::::::::M     M:::::::::::M  I::::I   U:::::D     D:::::U 
# M:::::::M::::M   M::::M:::::::M  I::::I   U:::::D     D:::::U 
# M::::::M M::::M M::::M M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M  M::::M::::M  M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M   M:::::::M   M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M    M:::::M    M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M     MMMMM     M::::::MII::::::IINU:::::UUUUUU:::::U 
# M::::::M               M::::::MI::::::::IU:::::::::::::::UU  
# M::::::M               M::::::MI::::::::IU:::::::::::::::UU  
# M::::::M               M::::::MIIIIIIIIIUUUUUUUUUUUUUUUUUUUU  
"""

attacksign = """
################################################################
#       ___           ___           ___           ___     
#      /\  \         /\  \         /\  \         /\__\    
#     /::\  \       /::\  \       /::\  \       /:/  /    
#    /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/  /     
#   /:/  \:\  \   /:/  \:\  \   /:/  \:\  \   /:/  /  ___ 
#  /:/__/ \:\__\ /:/__/ \:\__\ /:/__/ \:\__\ /:/__/  /\__\/
#  \:\  \  \/__/ \:\  \ /:/  / \:\  \ /:/  / \:\  \ /:/  /
#   \:\  \        \:\  /:/  /   \:\  /:/  /   \:\  /:/  / 
#    \:\  \        \:\/:/  /     \:\/:/  /     \:\/:/  /  
#     \:\__\        \::/  /       \::/  /       \::/__/   
#      \/__/         \/__/         \/__/         ~~    
################################################################
"""

