import ahkab
import numpy as np

Circuit = ahkab.Circuit('Circuit solution')
NetlistName = input('Pls enter netlist name\n')

File = open(NetlistName + '.txt', "r")

cccsBatteryCount = 1000  # counter to solve problem of repeating same node and name of empty battery in case of many ccsources in circuit by generating new node numbers
ccvsBatteryCount = 2000  # counter to solve problem of repeating same node and name of empty battery in case of many ccsources in circuit by generating new node numbers
NumOfCCsources = 0
Dependent = []
DependON = []

ElemID = []
VsID = []

for line in File:
    Inputs = line.split()
    if len(Inputs) > 0:
        if Inputs[0][0] == 'R':
            Circuit.add_resistor(Inputs[0], Inputs[1], Inputs[2], float(Inputs[3]))
        elif Inputs[0][0] == 'C':
            Circuit.add_capacitor(Inputs[0], Inputs[1], Inputs[2], float(Inputs[3]))
        elif Inputs[0][0] == 'L':
            Circuit.add_inductor(Inputs[0], Inputs[1], Inputs[2], float(Inputs[3]))
        elif Inputs[0][0] == 'V':
            real = float(Inputs[3]) * np.math.cos((np.math.pi) * float(Inputs[4]) / 180)
            imaginary = float(Inputs[3]) * np.math.sin((np.math.pi) * float(Inputs[4]) / 180)
            Circuit.add_vsource(Inputs[0], Inputs[1], Inputs[2], dc_value=0, ac_value=complex(real, imaginary))
        elif Inputs[0][0] == 'I':
            real = float(Inputs[3]) * np.math.cos((np.math.pi) * float(Inputs[4]) / 180)
            imaginary = float(Inputs[3]) * np.math.sin((np.math.pi) * float(Inputs[4]) / 180)
            Circuit.add_isource(Inputs[0], Inputs[1], Inputs[2], dc_value=0, ac_value=complex(real, imaginary))
        elif Inputs[0][0] == 'W':
            omega = float(Inputs[1])
            frequency = float(Inputs[1])/(2*np.math.pi)
        elif Inputs[0][0] == 'E':
            Circuit.add_vcvs(Inputs[0], Inputs[1], Inputs[2], Inputs[3], Inputs[4], value=float(Inputs[5]))
        elif Inputs[0][0] == 'G':
            Circuit.add_vccs(Inputs[0], Inputs[1], Inputs[2], Inputs[3], Inputs[4], value=float(Inputs[5]))
        elif Inputs[0][0] == 'F':
            DependON.append(Inputs[3])
            Dependent.append(line)
            NumOfCCsources += 1
        elif Inputs[0][0] == 'H':
            DependON.append(Inputs[3])
            Dependent.append(line)
            NumOfCCsources += 1
File.close()

# We have splited reading the File to two parts
# Because when you add H or F you remove the elem it depends on to rearrange nodes
# what if this elem hasn't been added yet, you are then going to remove an elem which is not added which gives a Value_Error
# This occures if the elem was written in the netlist before the F or H they depend on

File = open(NetlistName + '.txt', "r+")
sources = []
for line in File:
    LINE = line.split()
    if len(LINE) > 0:
        for x in range(NumOfCCsources):
            if Dependent[x].split()[3] == LINE[0]:
                Inputs = Dependent[x].split()
                ReqNode1 = LINE[1]
                ReqNode2 = LINE[2]

                if Inputs[0][0] == 'F':
                    if (len(Inputs) == 5):
                        if LINE[0][0] == 'V':
                            Circuit.add_cccs(Inputs[0], Inputs[1], Inputs[2], LINE[0], float(Inputs[4]))
                        elif LINE[0][0] == 'I':
                            real = float(LINE[3]) * np.math.cos((np.math.pi) * float(LINE[4]) / 180)
                            imaginary = float(LINE[3]) * np.math.sin((np.math.pi) * float(LINE[4]) / 180)
                            Circuit.remove_elem(LINE[0])
                            Circuit.add_isource(LINE[0], ReqNode1, str(cccsBatteryCount), dc_value=0,
                                                ac_value=complex(real, imaginary))
                            Circuit.add_vsource('V' + str(cccsBatteryCount), str(cccsBatteryCount), ReqNode2, dc_value=0,
                                                ac_value=0)
                            Circuit.add_cccs(Inputs[0], Inputs[1], Inputs[2], 'V' + str(cccsBatteryCount), float(Inputs[4]))
                            ElemID.append(Inputs[3])
                            VsID.append('V' + str(cccsBatteryCount))
                            cccsBatteryCount += 1
                        else:
                            ReqValue = float(LINE[3])
                            Circuit.remove_elem(LINE[0])
                            if LINE[0][0] == 'R':
                                Circuit.add_resistor(LINE[0], ReqNode1, str(cccsBatteryCount), ReqValue)
                                Circuit.add_vsource('V' + str(cccsBatteryCount), str(cccsBatteryCount), ReqNode2,
                                                    dc_value=0, ac_value=0)
                            elif LINE[0][0] == 'C':
                                Circuit.add_capacitor(LINE[0], ReqNode1, str(cccsBatteryCount), ReqValue)
                                Circuit.add_vsource('V' + str(cccsBatteryCount), str(cccsBatteryCount), ReqNode2,
                                                    dc_value=0, ac_value=0)
                            elif LINE[0][0] == 'L':
                                Circuit.add_inductor(LINE[0], ReqNode1, str(cccsBatteryCount), ReqValue)
                                Circuit.add_vsource('V' + str(cccsBatteryCount), str(cccsBatteryCount), ReqNode2,
                                                    dc_value=0, ac_value=0)
                            Circuit.add_cccs(Inputs[0], Inputs[1], Inputs[2], 'V' + str(cccsBatteryCount), float(Inputs[4]))
                            ElemID.append(Inputs[3])
                            VsID.append('V' + str(cccsBatteryCount))
                            cccsBatteryCount += 1
                    if (len(Inputs) == 6):
                        i = 0
                        if LINE[0][0] == 'V':
                            Circuit.add_cccs(Inputs[0], Inputs[1], Inputs[2], LINE[0], float(Inputs[4]))
                        else:
                            while(i < len(ElemID)):
                                if(ElemID[i]==Inputs[3]):
                                    Circuit.add_cccs(Inputs[0], Inputs[1], Inputs[2], VsID[i],
                                                     float(Inputs[4]))
                                i+= 1
                if Inputs[0][0] == 'H':
                    if(len(Inputs) == 5):
                        if LINE[0][0] == 'V':
                            Circuit.add_ccvs(Inputs[0], Inputs[1], Inputs[2], LINE[0], float(Inputs[4]))
                        elif LINE[0][0] == 'I':
                            real = float(LINE[3]) * np.math.cos((np.math.pi) * float(LINE[4]) / 180)
                            imaginary = float(LINE[3]) * np.math.sin((np.math.pi) * float(LINE[4]) / 180)
                            Circuit.remove_elem(LINE[0])
                            Circuit.add_isource(LINE[0], ReqNode1, str(ccvsBatteryCount), dc_value=0,
                                                ac_value=complex(real, imaginary))
                            Circuit.add_vsource('V' + str(ccvsBatteryCount), str(ccvsBatteryCount), ReqNode2, dc_value=0,
                                                ac_value=0)
                            Circuit.add_ccvs(Inputs[0], Inputs[1], Inputs[2], 'V' + str(ccvsBatteryCount), float(Inputs[4]))
                            ElemID.append(Inputs[3])
                            VsID.append('V' + str(ccvsBatteryCount))
                            ccvsBatteryCount += 1
                        else:
                            ReqValue = float(LINE[3])
                            Circuit.remove_elem(LINE[0])
                            if LINE[0][0] == 'R':
                                Circuit.add_resistor(LINE[0], ReqNode1, str(ccvsBatteryCount), ReqValue)
                                Circuit.add_vsource('V' + str(ccvsBatteryCount), str(ccvsBatteryCount), ReqNode2,
                                                    dc_value=0, ac_value=0)
                            elif LINE[0][0] == 'C':
                                Circuit.add_capacitor(LINE[0], ReqNode1, str(ccvsBatteryCount), ReqValue)
                                Circuit.add_vsource('V' + str(ccvsBatteryCount), str(ccvsBatteryCount), ReqNode2,
                                                    dc_value=0, ac_value=0)
                            elif LINE[0][0] == 'L':
                                Circuit.add_inductor(LINE[0], ReqNode1, str(ccvsBatteryCount), ReqValue)
                                Circuit.add_vsource('V' + str(ccvsBatteryCount), str(ccvsBatteryCount), ReqNode2,
                                                    dc_value=0, ac_value=0)
                            Circuit.add_ccvs(Inputs[0], Inputs[1], Inputs[2], 'V' + str(ccvsBatteryCount), float(Inputs[4]))
                            ElemID.append(Inputs[3])
                            VsID.append('V' + str(ccvsBatteryCount))
                            ccvsBatteryCount += 1
                    if (len(Inputs) == 6):
                        i = 0
                        if LINE[0][0] == 'V':
                            Circuit.add_ccvs(Inputs[0], Inputs[1], Inputs[2], LINE[0], float(Inputs[4]))
                        else:
                            while (i < len(ElemID)):
                                if (ElemID[i] == Inputs[3]):
                                    Circuit.add_ccvs(Inputs[0], Inputs[1], Inputs[2], VsID[i],
                                                     float(Inputs[4]))
                                i += 1

File.close()
ac = ahkab.new_ac(start=frequency, stop=frequency, points=2, x0=None)
solution = ahkab.run(Circuit, ac)
########################################################################################################################

PowerList = []
File = open(NetlistName + ".txt", "r")
Lines = File.readlines()
File.close()

File = open(NetlistName + ".txt", "r")
ResultFile = open("OutputFile.txt", 'w')
for line in File:
    Element = line.split()
    if len(Element) > 0:
        if Element[0][0] == 'R':
            if Element[2] != '0' and Element[1] != '0':
                voltageacross = (solution['ac']['V' + Element[1]][1] - solution['ac']['V' + Element[2]][1])
                PowerList.append(
                    (voltageacross * voltageacross.conjugate())
                    / (2 * float(
                        Element[3])))
                ResultFile.write("Active Power(" + Element[0] + ')= ' + str(
                    (voltageacross * voltageacross.conjugate())
                    / (2 * float(
                        Element[3]))) + ' WATT' + '\n')
            else:
                if Element[1] == '0':
                    voltageacross = solution['ac']['V' + Element[2]][1]
                else:
                    voltageacross = solution['ac']['V' + Element[1]][1]
                PowerList.append(
                    (voltageacross * voltageacross.conjugate()) / (2 * float(
                        Element[3])))
                ResultFile.write(
                    "Active Power(" + Element[0] + ')= ' + str(
                        (voltageacross * voltageacross.conjugate()) / (2 * float(
                            Element[3]))) + ' WATT' + '\n')
        elif Element[0][0] == 'C':
            impedance = 1 / (omega * complex(0, float(Element[3])))
            if Element[2] != '0' and Element[1] != '0':
                voltageacross = (solution['ac']['V' + Element[1]][1] - solution['ac']['V' + Element[2]][1])
                PowerList.append(
                    (voltageacross * voltageacross.conjugate())
                    / (2 * impedance.conjugate()))
                ResultFile.write("Reactive Power(" + Element[0] + ')= ' + str(
                    (voltageacross * voltageacross.conjugate())
                    / (2 * impedance.conjugate())) + ' VAR' + '\n')
            else:
                if Element[1] == '0':
                    voltageacross = solution['ac']['V' + Element[2]][1]
                else:
                    voltageacross = solution['ac']['V' + Element[1]][1]
                PowerList.append(
                    (voltageacross * voltageacross.conjugate()) / (2 * impedance.conjugate()))
                ResultFile.write(
                    "Reactive Power(" + Element[0] + ')= ' + str(
                        (voltageacross * voltageacross.conjugate()) / (2 * impedance.conjugate())) + ' VAR' + '\n')
        elif Element[0][0] == 'L':
            impedance = (omega * complex(0, float(Element[3])))
            IinInductor=solution['ac']['I('+Element[0]+')'][1]
            power=IinInductor*(IinInductor.conjugate())*impedance/2
            PowerList.append(power)
            ResultFile.write(
                "Reactive Power(" + Element[0] + ')= ' + str(power) + ' VAR'+ '\n')
        elif Element[0][0] == 'V':
            real = float(Element[3]) * np.math.cos((np.math.pi) * float(Element[4]) / 180)
            imaginary = float(Element[3]) * np.math.sin((np.math.pi) * float(Element[4]) / 180)
            power = 0.5 * ((solution['ac']['I(' + Element[0] + ')'][1]).conjugate()) * complex(real, imaginary)
            PowerList.append(power)
            ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
        elif Element[0][0] == 'I':
            if Element[1] == '0':
                real = float(Element[3]) * np.math.cos((np.math.pi) * float(Element[4]) / 180)
                imaginary = float(Element[3]) * np.math.sin((np.math.pi) * float(Element[4]) / 180)
                power = 0.5 * (solution['ac']['V' + Element[2]][1]) * (complex(real, imaginary).conjugate())  #########
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power)+ ' VA' + '\n')
            elif Element[2] == '0':
                real = float(Element[3]) * np.math.cos((np.math.pi) * float(Element[4]) / 180)
                imaginary = float(Element[3]) * np.math.sin((np.math.pi) * float(Element[4]) / 180)
                power = 0.5 * (solution['ac']['V' + Element[1]][1]) * (complex(real, imaginary).conjugate())  #########
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power)+ ' VA' + '\n')
            else:
                real = float(Element[3]) * np.math.cos((np.math.pi) * float(Element[4]) / 180)
                imaginary = float(Element[3]) * np.math.sin((np.math.pi) * float(Element[4]) / 180)
                power = 0.5 * (solution['ac']['V' + Element[2]][1] - solution['ac']['V' + Element[1]][1]) * (
                    complex(real, imaginary).conjugate())
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
        elif Element[0][0] == 'G':
            # vccs
            if Element[1] != '0' and Element[2] != '0' and Element[3] != '0' and Element[4] != '0':
                power = (solution['ac']['V' + Element[1]][1] - solution['ac']['V' + Element[2]][1]) * float(
                    Element[5]) * (
                            (solution['ac']['V' + Element[3]][1] - solution['ac']['V' + Element[4]][1]).conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[1] != '0' and Element[2] != '0' and Element[3] == '0':
                power = (solution['ac']['V' + Element[1]][1] - solution['ac']['V' + Element[2]][1]) * float(
                    Element[5]) * ((solution['ac']['V' + Element[4]][1]).conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[1] != '0' and Element[2] != '0' and Element[4] == '0':
                power = (solution['ac']['V' + Element[1]][1] - solution['ac']['V' + Element[2]][1]) * float(
                    Element[5]) * ((solution['ac']['V' + Element[3]][1]).conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[1] == '0':
                if Element[3] != '0' and Element[4] != '0':
                    power = (solution['ac']['V' + Element[2]][1]) * (float(Element[5])) * (
                        ((solution['ac']['V' + Element[3]][1]) - (solution['ac']['V' + Element[4]][1])).conjugate()) / 2
                    PowerList.append(power)
                    ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
                elif Element[3] == '0':
                    power = (solution['ac']['V' + Element[2]][1]) * float(Element[5]) * (
                        (solution['ac']['V' + Element[4]][1]).conjugate()) / 2
                    PowerList.append(power)
                    ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
                elif Element[4] == '0':
                    power = (solution['ac']['V' + Element[2]][1]) * float(Element[5]) * (
                        (solution['ac']['V' + Element[3]][1]).conjugate()) / 2
                    PowerList.append(power)
                    ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[2] == '0':
                if Element[3] != '0' and Element[4] != '0':
                    power = (solution['ac']['V' + Element[1]][1]) * float(Element[5]) * (
                        ((solution['ac']['V' + Element[3]][1]) - (solution['ac']['V' + Element[4]][1])).conjugate()) / 2
                    PowerList.append(power)
                    ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
                elif Element[3] == '0':
                    power = (solution['ac']['V' + Element[1]][1]) * float(Element[5]) * (
                        (solution['ac']['V' + Element[4]][1]).conjugate()) / 2
                    PowerList.append(power)
                    ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
                elif Element[4] == '0':
                    power = (solution['ac']['V' + Element[1]][1]) * float(Element[5]) * (
                        (solution['ac']['V' + Element[3]][1]).conjugate()) / 2
                    PowerList.append(power)
                    ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
        elif Element[0][0] == 'E':
            # vcvs
            IinE = solution['ac']['I(' + Element[0] + ')'][1]
            if Element[1] != '0' and Element[2] != '0':
                power = (solution['ac']['V' + Element[1]][1] - solution['ac']['V' + Element[2]][1]) * (
                    IinE.conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[1] == '0':
                power = (solution['ac']['V' + Element[2]][1]) * (IinE.conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[2] == '0':
                power = (solution['ac']['V' + Element[1]][1]) * (IinE.conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
        elif Element[0][0] == 'H':
            # The negative node must be before the positive one in the netlist
            # ccvs
            IinH = solution['ac']['I(' + Element[0] + ')'][1]
            if Element[1] != '0' and Element[2] != '0':
                power = (solution['ac']['V' + Element[1]][1] - solution['ac']['V' + Element[2]][1]) * (
                    IinH.conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[1] == '0':
                power = (solution['ac']['V' + Element[2]][1]) * (IinH.conjugate()) / 2
                PowerList.append(power)
                print(solution['ac']['V' + Element[2]][1])
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
            elif Element[2] == '0':
                power = (solution['ac']['V' + Element[1]][1]) * (IinH.conjugate()) / 2
                PowerList.append(power)
                ResultFile.write("Complex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')
File.close()

# Calculating the cccs's power
File = open(NetlistName + ".txt", "r")
for line in File:
    ReqPowerInF = line.split()
    if len(ReqPowerInF) > 0:
        for x in range(NumOfCCsources):
            if Dependent[x].split()[3] == ReqPowerInF[0]:
                Element = Dependent[x].split()
                if Element[0][0] == 'F':
                    # cccs
                    if ReqPowerInF[0][0] == 'V':
                        if (Element[1] != '0' and Element[2] != '0'):
                            power = ((solution['ac']['V' + Element[1]][1]) - (
                                solution['ac']['V' + Element[2]][1])) * (float(
                                Element(4))) * ((solution['ac']['I(' + ReqPowerInF[0] + ')'][1]).conjugate()) / 2
                        elif (Element[1] == '0'):
                            power = (solution['ac']['V' + Element[2]][1]) * (
                                float(
                                    Element(4))) * (
                                        (solution['ac']['I(' + ReqPowerInF[0] + ')'][1]).conjugate()) / 2
                        elif (Element[2] == '0'):
                            power = (solution['ac']['V' + Element[1]][1]) * (
                                float(
                                    Element(4))) * (
                                        (solution['ac']['I(' + ReqPowerInF[0] + ')'][1]).conjugate()) / 2
                    elif ReqPowerInF[0][0] == 'I':
                        real = float(ReqPowerInF[3]) * np.math.cos((np.math.pi) * (float(ReqPowerInF[4])) / 180)
                        imaginary = float(ReqPowerInF[3]) * np.math.sin(
                            (np.math.pi) * (float(ReqPowerInF[4])) / 180)
                        if (Element[1] != '0' and Element[2] != '0'):
                            power = ((solution['ac']['V' + Element[1]][1]) - (
                                solution['ac']['V' + Element[2]][1])) * float(
                                Element(4)) * (complex(real, imaginary).conjugate()) / 2
                        elif (Element[1] == '0'):
                            power = ((solution['ac']['V' + Element[2]][1])) * float(
                                Element(4)) * (complex(real, imaginary).conjugate()) / 2
                        elif (Element[2] == '0'):
                            power = ((solution['ac']['V' + Element[1]][1])) * float(
                                Element(4)) * (complex(real, imaginary).conjugate()) / 2
                    else:
                        if ReqPowerInF[0][0] == 'R':
                            if (ReqPowerInF[1] != '0' and ReqPowerInF[2] != '0'):
                                IinR = ((solution['ac']['V' + ReqPowerInF[1]][1]) - (
                                    solution['ac']['V' + ReqPowerInF[2]][
                                        1])) / float(ReqPowerInF[3])
                            elif (ReqPowerInF[1] == '0'):
                                IinR = ((solution['ac']['V' + ReqPowerInF[2]][
                                    1])) / float(ReqPowerInF[3])
                            elif (ReqPowerInF[2] == '0'):
                                IinR = ((solution['ac']['V' + ReqPowerInF[1]][
                                    1])) / float(ReqPowerInF[3])
                            if (Element[1] != '0' and Element[2] != '0'):
                                power = ((solution['ac']['V' + Element[1]][1]) - (
                                    solution['ac']['V' + Element[2]][1])) * (float(Element[4])) * (
                                            IinR.conjugate()) / 2
                            elif (Element[1] == '0'):
                                power = ((solution['ac']['V' + Element[2]][1])) * (float(Element[4])) * (
                                    IinR.conjugate()) / 2
                            elif (Element[2] == '0'):
                                power = ((solution['ac']['V' + Element[1]][1])) * (float(Element[4])) * (
                                    IinR.conjugate()) / 2
                        elif ReqPowerInF[0][0] == 'C':
                            ImpOfC = complex(0, -1 / (float(ReqPowerInF[3]) * omega))
                            if (ReqPowerInF[1] != '0' and ReqPowerInF[2] != '0'):
                                IinC = ((solution['ac']['V' + ReqPowerInF[1]][1]) - (
                                    solution['ac']['V' + ReqPowerInF[2]][
                                        1])) / ImpOfC
                            elif (ReqPowerInF[1] == '0'):
                                IinC = ((solution['ac']['V' + ReqPowerInF[2]][
                                    1])) / ImpOfC
                            elif (ReqPowerInF[2] == '0'):
                                IinC = ((solution['ac']['V' + ReqPowerInF[1]][
                                    1])) / ImpOfC
                            if (Element[1] != '0' and Element[2] != '0'):
                                power = ((solution['ac']['V' + Element[1]][1]) - (
                                    solution['ac']['V' + Element[2]][1])) * (float(Element[4])) * (
                                            IinC.conjugate()) / 2
                            elif (Element[1] == '0'):
                                power = (solution['ac']['V' + Element[2]][1]) * (float(Element[4])) * (
                                    IinC.conjugate()) / 2
                            elif (Element[2] == '0'):
                                power = ((solution['ac']['V' + Element[1]][1])) * (float(Element[4])) * (
                                    IinC.conjugate()) / 2
                        elif ReqPowerInF[0][0] == 'L':
                            IinL = (solution['ac']['I(' + ReqPowerInF[0] + ')'][1])
                            if (Element[1] != '0' and Element[2] != '0'):
                                power = ((solution['ac']['V' + Element[1]][1]) - (
                                    solution['ac']['V' + Element[2]][1])) * (float(Element[4])) * (
                                            IinL.conjugate()) / 2
                            elif (Element[1] == '0'):
                                power = ((solution['ac']['V' + Element[2]][1])) * (float(Element[4])) * (
                                    IinL.conjugate()) / 2
                            elif (Element[2] == '0'):
                                power = ((solution['ac']['V' + Element[1]][1])) * (float(Element[4])) * (
                                    IinL.conjugate()) / 2
                    PowerList.append(power)
                    ResultFile.write("Comlex Power(" + Element[0] + ')= ' + str(power) + ' VA'+ '\n')

File.close()


File = open(NetlistName + ".txt", "r")
Max=0
for line in File:
    CurrentLine=line.split()
    if len(CurrentLine) > 2:
        if(float(CurrentLine[1]) > Max):
            Max = float(CurrentLine[1])
        if(float(CurrentLine[2]) > Max):
            Max = float(CurrentLine[2])

i=1
while i<=Max :
    ResultFile.write('\n'+"Voltage of Node"+str(i)+" ="+str(solution['ac']['V'+str(i)][1]) + ' Volts')
    i+=1

File.close()
ResultFile.close()