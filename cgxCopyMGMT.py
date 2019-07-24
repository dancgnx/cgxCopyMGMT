#!/usr/bin/env python3

import cloudgenix
from cloudgenix import jd, jd_detailed
import cgxinit
import sys
import logging
import csv

def getElementByName(cgx,name):
    """
    get Element json object by using the element name
    """
    res = cgx.get.elements()
    if not res.cgx_status:
        print(res.cgx_content)
        raise ValueError(f"Can't retrieve element {name}")
    for item in res.cgx_content["items"]:
        if item["name"] == name:
            return item
    return None
def getInterfaceByName(cgx,site_id,element_id,name):
    """
    get Interface json object by using the interface name
    """
    res = cgx.get.interfaces(site_id=site_id,element_id=element_id)
    if not res.cgx_status:
        print(res.cgx_content)
        raise ValueError(f"Can't retrieve interface {name}")
    for item in res.cgx_content["items"]:
        if item["name"] == name:
            return item
    return None

def getDeviceManagementExtensionByInterface(cgx,site_id,element_id,interface_id):
    """
    get the existing config for the interface
    """
    res = cgx.get.element_extensions(site_id=site_id,element_id=element_id)
    if not res.cgx_status:
        print(res.cgx_content)
        raise ValueError(f"Can't retrieve element extensions")
    for item in res.cgx_content["items"]:
        if item["namespace"] == "devicemanagement/interface" and item["entity_id"] == interface_id:
            return item
    return None

def pasteDeviceManagementAccessToInterface(cgx,s_ext,t_elementname,t_interfacename):
    """
    apply source extension json object to the interface
    """

    log.info(f"Copy to interface {t_interfacename} of element {t_elementname}")

    # get interface details
    t_element = getElementByName(cgx,t_elementname)
    if not t_element:
        log.error(f"----- Couldn't find target element {t_elementname}")
        sys.exit(-1)
    t_eid = t_element["id"]
    t_siteid = t_element["site_id"]
    t_interface = getInterfaceByName(cgx,t_siteid,t_eid,t_interfacename)
    if not t_interface:
        log.error(f"----- Couln't find target interface {t_interfacename} of element {t_elementname}")
        sys.exit(-1)
    t_interfaceid = t_interface["id"]

    # if extension already exists, delete it
    t_ext = getDeviceManagementExtensionByInterface(cgx,t_siteid,t_eid,t_interfaceid)
    if t_ext:
        log.info("------ Deleting existing Device Management configuration from the interface")
        res = cgx.delete.element_extensions(t_siteid,t_eid,t_ext["id"])
        if not res:
            log.error(f"----- Can't delete existing extension from interface {t_interfacename}. Error {res.cgx_content}")
            sys.exit(-1)
    
    # build the extension structure
    t_ext = {     
        "name": s_ext["name"],
        "namespace": "devicemanagement/interface",
        "entity_id": t_interfaceid,
        "disabled": s_ext["disabled"],
        "conf": s_ext["conf"]
        }    
    
    # add the extension to the interfaces
    res = cgx.post.element_extensions(t_siteid, t_eid,t_ext)
    if not res:
        log.error(f"----- Couln't add extension. Error {res.cgx_content}")
        sys.exit(-1)
    log.info("----- Success")

if __name__ == "__main__":
    # initiate cgx objext and get ommand line arguments
    cgx, args = cgxinit.go()

    #init logging
    logging.basicConfig(level=logging.INFO)
    log=logging.getLogger("cgxCopyMGMT")

    #parse arguments
    s_element = getElementByName(cgx,args["s_element"])
    if not s_element:
        log.error(f"Couldn't find source element {args['s_element']}")
        sys.exit(-1)
    s_eid = s_element["id"]
    s_siteid = s_element["site_id"]
    s_interface = getInterfaceByName(cgx,s_siteid,s_eid,args["s_interface"])
    if not s_interface:
        log.error(f"Couln't find source interface {args['s_interface']} of element {args['s_element']}")
        sys.exit(-1)
    s_interfaceid = s_interface["id"]

    # get existing device access policy for the source interface
    s_ext = getDeviceManagementExtensionByInterface(cgx,s_siteid,s_eid,s_interfaceid)
    if not s_ext:
        log.error("Source interface has no configurations")
        sys.exit(-1)
    
    if args["list"]:
        jd(s_ext)
    elif args["t_element"] and args["t_interface"]:
        # update a single target
        pasteDeviceManagementAccessToInterface(cgx,s_ext,args["t_element"],args["t_interface"])
    elif args["interface_file"]:
        # read targets from file
        with open(args["interface_file"]) as f:
            interfaces = csv.reader(f)
            for interface in interfaces:
                # check if there are two and only two items in each line
                if len(interface) != 2:
                    log.error(f"Invalid line. Should have 'element name,interfacename' but got {','.join(interface)}")
                    sys.exit(-1)
                # update a single interface
                pasteDeviceManagementAccessToInterface(cgx,s_ext,interface[0],interface[1])
    else:
        # if we reached here, then the wrong combination of parameters where used
        print ("ERROR: You must specify target element and target itnerface or a file with list of targets")
