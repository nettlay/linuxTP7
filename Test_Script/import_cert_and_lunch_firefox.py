import pyautogui
import time
import cv2
import os
import datetime
import sys
import subprocess
def get_position(img,region,similaity=0.98):
    img=os.path.join(os.getcwd(),"Test_Data","import_cert_and_lunch_firefox",img)
    print(img)
    print(img)
    count=5
    count1=count
    while count:
        part_img = cv2.imread(img, 0)
        w, h = part_img.shape[::-1]
        if region is None:
            pyautogui.screenshot().save("temp.png")
            full_img= cv2.imread("temp.png", 0)
            res = cv2.matchTemplate(part_img, full_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val >similaity:
                print("find :" + img + " with similaity " + str(max_val) + " in full screen")
                logs("find :" + img + " with similaity " + str(max_val) + " in full screen")
                return (max_loc[0],max_loc[1],w,h),(int(max_loc[0]+w/2),int(max_loc[1]+h/2))
        else:
            pyautogui.screenshot(region=region).save("temp.png")
            full_img = cv2.imread("temp.png",0)
            res = cv2.matchTemplate(part_img, full_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val >similaity:
                print("find :"+img+" with similaity "+str(max_val)+"in region:"+str(region))
                logs("find :"+img+" with similaity "+str(max_val)+"in region:"+str(region))
                return (max_loc[0],max_loc[1],w,h),(int(max_loc[0]+w/2),int(max_loc[1]+h/2))
        count = count - 1
        print("can not find :" + img + " :wait 1s repeat")
        logs("can not find :" + img + " :wait 1s repeat")
    print("can not find " + img + " in "+str(count1)+" repeats")
    logs("can not find " + img + " in "+str(count1)+" repeats")
    return False
def logs(strs):
    log_path=os.path.join(os.getcwd(),"Log")
    strs=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"_"+str(strs)+"\n"
    if os.path.exists(log_path):
        f=open(os.path.join(log_path,"log.txt"),"a",encoding="utf-8")
        f.writelines(strs)
        f.close()
    else:
        os.mkdir(log_path)
        f=open(os.path.join(log_path,"log.txt"),"a",encoding="utf-8")
        f.writelines(strs)
        f.close()
def thinpro_import_cert():
    # pb=position_box
    # pc=position_center
    logs("thinpro_import_cert start")
    print("thinpro_import_cert start")
    RootCA_cert_path=os.path.join(os.getcwd(),"Test_Data","import_cert_and_lunch_firefox","RootCA_path.txt")
    if os.path.exists(RootCA_cert_path):
        content=open(RootCA_cert_path,'r')
        path=content.readline().strip().replace("\n","")
    else:
        print("can not find RootCA")
        logs("can not find RootCA")
        sys.exit()

    start_button=get_position("start_button.png",None)
    if start_button:
        start_button_pb,start_button_pc=start_button
        pyautogui.click(start_button_pc)

        control_panel_button=get_position("control_panel_button.png",None)
        if control_panel_button:
            control_panel_button_pb,control_panel_button_pc=control_panel_button
            pyautogui.click(control_panel_button_pc)

            control_panel=get_position("control_panel.png",None)
            if control_panel:
                control_panel_pb,control_panel_pc=control_panel
                security = get_position("security.png", None)
                if security:
                    security_pb, security_pc = security
                    pyautogui.click(security_pc)

                    certificate = get_position("certificate.png", None)
                    if certificate:
                        certificate_pb, certificate_pc = certificate
                        pyautogui.click(certificate_pc)

                        local_root = get_position("local_root.png", None)
                        if local_root:
                            local_root_pb, local_root_pc = local_root
                            pyautogui.click(local_root_pc)
                        else:
                            local_root = get_position("local_root_gray.png", None)
                            if local_root:
                                local_root_pb, local_root_pc = local_root
                                pyautogui.click(local_root_pc)
                            else:
                                print("can not find local root")
                                logs("can not find local root")

                        if local_root:
                                import_from_url = get_position("import_from_url.png", None)
                                if import_from_url:
                                    import_from_url_pb, import_from_url_pc = import_from_url
                                    pyautogui.click(import_from_url_pc)
                                    cert_import = get_position("cert_import.png", None)
                                    if cert_import:
                                        cert_import_pb, cert_import_pc = cert_import
                                        cert_import_url = get_position("cert_import_url.png", None)
                                        if cert_import_url:
                                            cert_import_url_pb, cert_import_url_pc = cert_import_url
                                            pyautogui.click(cert_import_url_pc)
                                            pyautogui.typewrite(path)


                                            cert_import_button = get_position("cert_import_button.png", None)
                                            if cert_import_button:
                                                cert_import_button_pb, cert_import_button_pc = cert_import_button
                                                pyautogui.click(cert_import_button_pc)
                                                print("wait 10s for import cert")
                                                logs("wait 10s for import cert")
                                                time.sleep(10)
                                                cert_import_success = get_position("cert_import_success.png", None)
                                                if cert_import_success:
                                                    cert_import_success_pb, cert_import_success_pc = cert_import_success
                                                    print("import success")
                                                    logs("import success")

                                                else:
                                                    cert_import_fail_exist= get_position("cert_import_fail_exist.png", None)
                                                    if cert_import_fail_exist:
                                                        cert_import_fail_exist_pb,cert_import_fail_exist_pc=cert_import_fail_exist
                                                        print("import fail ,cert_import_fail_exist")
                                                        logs("import fail ,cert_import_fail_exist")
                                                    else:
                                                        print("cert import fail ,others")
                                                        logs("cert import fail ,others")

                                            else:
                                                print("can not find cert_import_button")
                                                logs("can not find cert_import_button")

                                        else:
                                            print("can not find cert_import_url")
                                            logs("can not find cert_import_url")
                                    else:
                                        print("can not find cert_import")
                                        logs("can not find cert_import")
                                else:
                                    print("can not find import_from_url")
                                    logs("can not find import_from_url")
                else:
                    print("can not find security")
                    logs("can not find security")

            else:
                print("can not find control_panel")
                logs("can not find control_panel")

        else:
            print("can not find control_panel_button")
            logs("can not find control_panel_button")
    else:
        print("can not find start_button.png")
        logs("can not find start_button.png")

    if cert_import_success:
        close=get_position("close.png",cert_import_success_pb)
        if close:
            close_pb,close_pc=close
            close_pc_actual=close_pc[0]+cert_import_success_pb[0],close_pc[1]+cert_import_success_pb[1]
            pyautogui.click(close_pc_actual)
            print("find close in cert_import_fsuccess_pb success and close")
            logs("find close in cert_import_fsuccess_pb success and close")

    elif cert_import_fail_exist:
        close=get_position("close.png",cert_import_fail_exist_pb)
        if close:
            close_pb,close_pc=close
            close_pc_actual=close_pc[0]+cert_import_fail_exist_pb[0],close_pc[1]+cert_import_fail_exist_pb[1]
            pyautogui.click(close_pc_actual)
            print("find close in cert_import_fail_exist_pb success and close")
            logs("find close in cert_import_fail_exist_pb success and close")
        else:
            print("can not find close in cert_import_result_pb")
            logs("can not find close in cert_import_result_pb")

    if cert_import:
        close=get_position("close.png",cert_import_pb)
        if close:
            close_pb,close_pc=close
            close_pc_actual=close_pc[0]+cert_import_pb[0],close_pc[1]+cert_import_pb[1]
            pyautogui.click(close_pc_actual)
            print("find close in cert_import_pb and close")
            logs("find close in cert_import_pb and close")

    if control_panel:
        close=get_position("close.png",control_panel_pb)
        if close:
            close_pb,close_pc=close
            close_pc_actual=close_pc[0]+control_panel_pb[0],close_pc[1]+control_panel_pb[1]
            pyautogui.click(close_pc_actual)
            print("find close in control_panel and close")
            logs("find close in control_panel and close")

    if os.path.exists("temp.png"):
        os.unlink("temp.png")
    logs("thinpro_import_cert finish")
    print("thinpro_import_cert finish")
def thinpro_firefox_lunch():
    logs("thinpro_firefox_lunch start")
    print("thinpro_firefox_lunch start")
    ostest_ftp_path=os.path.join(os.getcwd(),"Test_Data","import_cert_and_lunch_firefox","ostest_ftp.txt")
    if os.path.exists(ostest_ftp_path):
        content=open(ostest_ftp_path,'r')
        path=content.readline().strip().replace("\n","")
    else:
        print("can not find ostestftp.txt")
        logs("can not find ostestftp.txt")
        sys.exit()

    firefox_lunch_Icon=get_position("firefox_lunch_Icon.png",None)
    if firefox_lunch_Icon:
        firefox_lunch_Icon_pb,firefox_lunch_Icon_pc=firefox_lunch_Icon
        pyautogui.doubleClick(firefox_lunch_Icon_pc)
        time.sleep(1)
        pyautogui.doubleClick(firefox_lunch_Icon_pc)
        time.sleep(5)
        firefox_input=get_position("firefox_input.png",None)
        if firefox_input:
            firefox_input_pb,firefox_input_pc=firefox_input
            pyautogui.click(firefox_input_pc,interval=0.1)
            time.sleep(1)
            pyautogui.click(firefox_input_pc, interval=0.1)
            pyautogui.typewrite(path)
            pyautogui.press("enter")
            firefox_finish=get_position("firefox_finish.png",None)
            if firefox_finish:
                firefox_finish_pb,firefox_input_pc=firefox_finish
                firefox_close=get_position("firefox_close.png",firefox_finish_pb)
                if firefox_close:
                    firefox_close_pb,firefox_close_pc=firefox_close
                    firefox_close_pc_actual=firefox_close_pc[0]+firefox_finish_pb[0],firefox_close_pc[1]+firefox_finish_pb[1]
                    pyautogui.click(firefox_close_pc_actual)
                    print("firefox_lunch close success")
                    logs("firefox_lunch close success")
                else:
                    print("can not find firefox_lunch close")
                    logs("can not find firefox_lunch close")
            else:
                print("can not find firefox_finish.png")
                logs("can not find firefox_finish.png")
        else:
            print("can not find firefox_input.png")
            logs("can not find firefox_input.png")
    else:
        print("can not find firefox_lunch_Icon.png")
        logs("can not find firefox_lunch_Icon.png")

    if os.path.exists("temp.png"):
        os.unlink("temp.png")
    logs("thinpro_firefox_lunch finish")
    print("thinpro_firefox_lunch finish")
def run_command_list(cmd):
    if not cmd:
        return
    subprocess.Popen(["/usr/bin/hptc-simple-xterm"])
    time.sleep(1)
    pyautogui.typewrite("su -")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite("1")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    for i in cmd:
        pyautogui.typewrite(i)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
    pyautogui.typewrite("exit")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.typewrite("exit")
    time.sleep(1)
    pyautogui.press("enter")
def thinpro_del_cert():
    CAname="ROOTCA"
    CApath="/usr/local/share/ca-certificates/"+CAname+".crt"
    CApath1="/etc/ssl/certs/"+CAname+".pem"
    cmd_list=[]
    if os.path.exists(CApath) :
        cmd_list.append("rm -rf "+CApath)
    if os.path.exists(CApath1):
        cmd_list.append("rm -rf "+CApath1)
    if cmd_list:
        cmd_list.append("mclient apply root/CertMgr")
        run_command_list(cmd_list)


# for i in range(0,1):
#
#     try:
#         thinpro_import_cert()
#     except Exception as e:
#         logs(str(e))
#     try:
#         thinpro_del_cert()
#     except Exception as e:
#         logs(str(e))
#     try:
#         thinpro_firefox_lunch()
#     except Exception as e:
#         logs(str(e))
#
#     print("finish:"+str(i))



