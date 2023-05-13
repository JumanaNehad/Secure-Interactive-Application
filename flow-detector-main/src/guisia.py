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

import asyncio
from asyncio import events
import subprocess
from selectors import EVENT_READ
from nicegui import ui
import database
import tkinter as tk
import pandas as pd
import tensorflow as tf
import numpy as np
import scapy.all as scapy
import asyncio
from threading import Thread, Event
from nicegui import ui
import importlib
import sys
import sniffer
import globalflags
from datetime import datetime
from train import DdosDetector

module_name = __name__

db = database.Database()
# Connect to MySQL and get cursor
conn, cur = db.connectdb()
gdata = []
gdatab = []
gdatab = db.fetch_black_list()
gdata = db.fetch_white_list()
ddosdetect = DdosDetector()
snifferobj = sniffer.Sniffer()
grid = None
gridb = None
# model = ddosdetect.load_model()
interface_textbox = None

async def block():
    global grid , gridb
    selected_rows = await grid.get_selected_rows()
    if selected_rows:
        for row in selected_rows:
            ui.notify(f"{row['ip']}")
            ipp = row['ip']
            db.insert_to_black_list(row['ip'])
            db.delete_white_list(row['ip'])
            # subprocess.call(f'netsh advfirewall firewall add rule name="Block IP {ipp}" dir=in action=block remoteip={ipp}')
            
        db.fetch_black_list()
        db.fetch_white_list()
        gdatab = db.fetch_black_list()
        gdata = db.fetch_white_list()
        gridb.update()
        grid.update()
        ui.update()
        ui.run()
        loadgui()
    else:
        ui.notify('No row selected!')
        gridb.update()
        grid.update()
        ui.update()

async def unblock():
    global grid , gridb
    selected_rows = await gridb.get_selected_rows()
    if selected_rows:
        for row in selected_rows:
            ui.notify(f"{row['ip']}")
            db.insert_to_white_list(row['ip'])
            db.delete_black_list(row['ip'])
            ipp = row['ip']
            # subprocess.call(f'netsh advfirewall firewall delete rule name="Block IP {ipp}')

        db.fetch_black_list()
        db.fetch_white_list()    
        gdatab = db.fetch_black_list()
        gdata = db.fetch_white_list()
        gridb.update()
        grid.update()
        ui.update()
        ui.run()
        loadgui()
    else:
        ui.notify('No row selected!')
        gridb.update()
        grid.update()
        ui.update()
    gdatab = db.fetch_black_list()
    gdata = db.fetch_white_list()
    gridb.update()
    grid.update()
    

async def start_sniffer():
    global interface_textbox
    ui.notify(f'its ON' )
    interface_textbox.set_text('its on' )
    await snifferobj.start()
    
def stop_sniffer():
    interface_textbox.set_text(f'its Off' )
    ui.notify(f'its Off' )
    snifferobj.stop()



async def reload_modules():
    
    for module in sys.modules.values():
        try:
            importlib.reload(module)
        except Exception as e:
            print(f"Error reloading {module.__name__}: {e}")

async def refreshgui():
    db.fetch_black_list()
    db.fetch_white_list()
    global gdata
    global gdatab

    
    gdatab = db.fetch_black_list()
    gdata = db.fetch_white_list()
    global grid , gridb
    gridb.update()
    grid.update()
    
    db.fetch_black_list()
    db.fetch_white_list()    
    gdatab = db.fetch_black_list()
    gdata = db.fetch_white_list()
    gridb.update()
    grid.update()
    ui.update()
    ui.run()
    loadgui()
    # ui.update()
    # ui.run()
    # import sys
    # sys.modules.clear(  )
    # import main
    # importlib.reload(ui)
    # importlib.reload(main)
    print("Refreshed GUI")
    ui.notify("Refreshed GUI")
    

    # await reload_modules()

async def deletewhite():
    global grid , gridb
    selected_rows = await grid.get_selected_rows()
    if selected_rows:
        for row in selected_rows:
            ui.notify(f"{row['ip']}")
            db.delete_white_list(row['ip'])
            loadgui()
    else:
        ui.notify('No row selected!')
            
async def deleteblack():
    global grid , gridb
    selected_rows = await gridb.get_selected_rows()
    if selected_rows:
        for row in selected_rows:
            ui.notify(f"{row['ip']}")
            db.delete_black_list(row['ip'])
            ipp = row['ip']
            subprocess.call(f'netsh advfirewall firewall delete rule name="Block IP {ipp}')
            loadgui()
    else:
        ui.notify('No row selected!')


def deleteall():
    if globalflags.stop_flag:
        
        
        print("deleted all")
        ui.notify("deleted all")
        ui.spinner()
        task1 = asyncio.create_task(db.delete_all())
        ui.update()
        ui.run()

        
    else:
        ui.notify("Stop Sniffing first")

async def retrain():
    if globalflags.stop_flag:
        print("Retraining")
        ui.notify("Retraining")
        ui.spinner()
        ui.update()
        ui.run()
        await ddosdetect.retrain()
    else:
        ui.notify("Stop Sniffing first")
ui.image(globalflags.logopathon).style('height:500; width:500')
label = ui.label("White List")
ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'))

def loadgui():
    label = ui.label("White List")
    global grid , gridb
    gdata = db.fetch_white_list()
    gdatab = db.fetch_black_list()
    grid = ui.aggrid({
            'columnDefs': [
                {'headerName': 'IP Address', 'field': 'ip'},
                {'headerName': 'Date Added', 'field': 'dateadded'}
            ],
            'rowData': gdata,
            'rowSelection': 'multiple',
        }).classes('max-h-40')
    with ui.row():
        ui.button('Block', on_click=block)
        ui.button('Select all', on_click=lambda: grid.call_api_method('selectAll'))
        ui.button('Delete Selected', on_click=deletewhite)


    ui.label("Black List")
    gridb = ui.aggrid({
        'columnDefs': [
            {'headerName': 'IP Address', 'field': 'ip'},
            {'headerName': 'Date Added', 'field': 'dateadded'}
        ],
        'rowData': gdatab,
        'rowSelection': 'multiple',
    }).classes('max-h-40')
    with ui.row():
        ui.button('UnBlock', on_click=unblock)
        ui.button('Select all', on_click=lambda: gridb.call_api_method('selectAll'))
        ui.button('Delete Selected', on_click=deleteblack)

    ui.label('Interface:')
    global interface_textbox
    interface_textbox = ui.label('Wi-Fi')

    with ui.row():
        
        buttonstart = ui.button(text='Start', on_click=start_sniffer)
        buttonstop = ui.button(text='Stop', on_click=stop_sniffer)
        ui.button(text='Restart',on_click=refreshgui)
        # ui.button(text='Delete All',on_click=deleteall)
        ui.button(text='Retrain',on_click=retrain)
        # ui.button(text='Exit',on_click=ui.c)
    print(globalflags.emblem)
    ui.run(title="SIA DDoS Detector",reload=True)

loadgui()
