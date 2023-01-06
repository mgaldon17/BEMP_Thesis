import sys
import time
import numpy as np
import os
import logging
from analysis import Analyzer
import queue
import re

# Configuration
d_0 = 0.0005 #Lowest density value in g/cm3
d_f = 0.0025 #Highest density value in g/cm3
INPUT_FILE_NAME = "input.txt"
OUTPUT = "output/"
q = queue.Queue()
datanames = []  # Datanames of the mctax files containing the dose info

class MCNP():

    def __init__(self, density):
        self.density = density
        self.input_file = '''MCNP Runfile for
                        C ****** 1.10.2022
                        C ****** Simulation of the ionization chamber type 33051
                        C ***************************************************************
                        C ******* Block A: Cells
                        7 2 -''' + self.density + ''' -1 6 -5 21               $Cell of wall (Ar)
                        8 1 -1.5914 -2 1 6 -5                                    $Cell of the outer wall (A-150)
                        9 1 -1.5914 -4 3 5                                       $Cell of the outermost cask wall (A-150)
                        10 2 -''' + self.density + ''' -3 5 22                 $Internal cask wall   
                        14 0 20                                                $Graveyard
                        15 1 -1.5914 -21 -5 6                                    $Innermost chamber
                        16 1 -1.5914 -22 5                                       $Innermost sphere
                        17 4 -0.9 -24 -6 23
                        18 3 -0.001205 -20 #17 #19 #8 #9 #7 #15 #16 #10
                        19 1 -1.5914 23 -25 24 -26
    
                        C ***************************************************************
                        C ***************************************************************
                        C Block B: Planes
                        C ***************************************************************
                        C Beginning of surfaces
                        1 CY 0.4
                        2 CY 0.7
                        3 SY 6.35 0.4
                        4 SY 6.35 0.7
                        5 PY 6.35
                        6 PY 4.25
                        21 CY 0.2
                        22 SY 6.35 0.2
                        23 PY 1
                        24 CY 0.75
                        25 CY 0.85
                        26 PY 1.5
                        20 RPP -60 60 -60 60 -60 60 $Outer world contour
                        
                        C ***************************************************************
                        C ***************************************************************
                        C Block C: Materials and source
                        C ***************************************************************
                        C Mg (d=1.5914 g/cm3) with 20% water
                        M1 12000.60c -0.8
                                1000.80c -0.02238
                                8000.80c -0.17762
                        C Ar gas (d=1.66201E-03 g/cm3) $0.2E-3, 0.5E-3, 1.06409E-3, 1.5E-3, 2E-3, 4E-4 8E-3, 1E-2, 3E-2
                        M2 18000.59c 1
                        C Dry air (d=0.001205 g/cm3)
                        M3 6012.80c -0.000124
                                7014.80c -0.755267
                                8016.80c -0.231781
                                18040.80c -0.012827
                        C Polyethlyene (d=0.9 g/cm3)
                        M4 1001.80c -0.143711
                                6000.80c -0.856289
                        C Water (d=0.997 g/cm3)
                        M5 1000.80c -0.11190
                                8000.80c -0.88810
                        C ***************************************************************
                        C ******** Source ***********************************************
                        sdef erg=fpar=d5
                             par=d4
                             pos= 50 6.5 0
                             x=50
                             y=d1
                             z=d2
                             vec=-1 0 0
                             dir=1
                        si1 6 7
                        sp1    0.   1.
                        si2 -1.0 1.0
                        sp2    0.   1.                        
                        c si3   -1 0.99943 1 $ acosd(0.99943)=1.9346
                        c sp3    0 0.999715 0.000285
                        c sb3 0 0 1
                        SI4 L 1  2 $Discrete lines od particles 1 and 2 (photons and neutrons)
                        SP4   3.25 3.74 $Distribution probabilities 
                        DS5 S 6 7  $Energy bins for neutrons and photons 
                        si6 h   1.00e-10            $// Energy-Bins Neutron
                                1.00E-09
                                1.00E-08
                                2.53E-08
                                5.00E-08
                                1.00E-07
                                2.00E-07
                                5.00E-07
                                1.00E-06
                                2.00E-06
                                5.00E-06
                                1.00E-05
                                2.00E-05
                                5.00E-05
                                1.00E-04
                                2.00E-04
                                5.00E-04
                                1.00E-03
                                2.00E-03
                                5.00E-03
                                1.00E-02
                                2.00E-02
                                3.00E-02
                                5.00E-02
                                7.00E-02
                                1.00E-01
                                1.50E-01
                                2.00E-01
                                3.00E-01
                                5.00E-01
                                7.00E-01
                                9.00E-01
                                1.00E+00
                                1.20E+00
                                2.00E+00
                                3.00E+00
                                4.00E+00
                                5.00E+00
                                6.00E+00
                                7.00E+00
                                8.00E+00
                                9.00E+00
                                1.00E+01
                        sp6 d   0.0
                                0.00000000000000001414
                                0.00000000000000922585
                                0.00000000000002933800
                                0.00000000000004041040
                                0.00000000000006834050
                                0.00000000000001891980
                                0.00000000000001048970
                                0.00000000000001391860
                                0.00000000000006182110
                                0.00000000000029278700
                                0.00000000000049868000
                                0.00000000000088352000
                                0.00000000000192086000
                                0.00000000000172683000
                                0.00000000000291760000
                                0.00000000000489084000
                                0.00000000000361733000
                                0.00000000000465964000
                                0.00000000000782809000
                                0.00000000000632571000
                                0.00000000000772910000
                                0.00000000000597985000
                                0.00000000000470697000
                                0.00000000000691685000
                                0.00000000000439179000
                                0.00000000001265570000
                                0.00000000000975152000
                                0.00000000001892580000
                                0.00000000003669340000
                                0.00000000005006590000
                                0.00000000004083790000
                                0.00000000001682890000
                                0.00000000004897530000
                                0.00000000017208000000
                                0.00000000012016000000
                                0.00000000005442450000
                                0.00000000003312610000
                                0.00000000002638510000
                                0.00000000001024140000
                                0.00000000001056000000
                                0.00000000000038659000
                                0.00000000000302253000
                        SI7 H   0.01                    $// Energie-Bins Photonen
                                0.0667
                                0.133
                                0.2
                                0.267
                                0.333
                                0.4
                                0.467
                                0.533
                                0.6
                                0.667
                                0.733
                                0.8
                                0.867
                                0.933
                                1.0
                                1.07
                                1.13
                                1.2
                                1.27
                                1.33
                                1.4
                                1.47
                                1.53
                                1.6
                                1.67
                                1.73
                                1.8
                                1.87
                                1.93
                                2.0
                                2.07
                                2.13
                                2.2
                                2.27
                                2.33
                                2.4
                                2.47
                                2.53
                                2.6
                                2.67
                                2.73
                                2.8
                                2.87
                                2.93
                                3.0
                                3.07
                                3.13
                                3.2
                                3.27
                                3.33
                                3.4
                                3.47
                                3.53
                                3.6
                                3.67
                                3.73
                                3.8
                                3.87
                                3.93
                                4.0
                                4.07
                                4.13
                                4.2
                                4.27
                                4.4
                                4.47
                                4.6
                                4.67
                                4.73
                                4.8
                                4.87
                                4.93
                                5.13
                                5.2
                                5.27
                                5.33
                                5.47
                                5.67
                                5.73
                                5.8
                                5.87
                                5.93
                                6.0
                                6.07
                                6.13
                                6.2
                                6.27
                                6.53
                                6.6
                                6.67
                                6.73
                                6.87
                                6.93
                                7.0
                                7.07
                                7.13
                                7.2
                                7.47
                                7.53
                                7.6
                                7.67
                                7.73
                                7.8
                                8.0
                                8.6
                                9.13
                        SP7 D   0.0                   $// Wahrscheinlichkeiten Photonen
                                0.001169719831418
                                0.002069497238404
                                0.001234279635802
                                0.002131315287795
                                0.003623677160095
                                0.007290145185376
                                0.013187516726444
                                0.024849827358639
                                0.021998456297642
                                0.025457587559632
                                0.026326937711310
                                0.029401330106360
                                0.029527726906121
                                0.028164427804627
                                0.029949410447937
                                0.030157139663819
                                0.023995769325134
                                0.025318740539766
                                0.025114529864349
                                0.023779785072008
                                0.021651474076456
                                0.020781176625423
                                0.019562002354492
                                0.018273133916669
                                0.019103103480840
                                0.016887640944553
                                0.015284539777559
                                0.015641671634701
                                0.014174981574944
                                0.013905948557893
                                0.013026624697284
                                0.013754651317922
                                0.011868239979300
                                0.057654398064996
                                0.011948002585059
                                0.008397389270994
                                0.008045738217268
                                0.008133945320142
                                0.011782252263488
                                0.008372976013310
                                0.007605176352576
                                0.006374472095200
                                0.008820074243557
                                0.005831398907360
                                0.014359434292368
                                0.010963961547089
                                0.006456941270547
                                0.004199770496908
                                0.006450756759038
                                0.004952927616171
                                0.005570417934834
                                0.009475564799236
                                0.004880486281147
                                0.008336518520959
                                0.003043794625858
                                0.005048361259845
                                0.003109496602607
                                0.006650596324571
                                0.005426414899902
                                0.003271051741317
                                0.002316390516225
                                0.001896818098688
                                0.009316134317653
                                0.009226384470113
                                0.005168208161203
                                0.003258642119756
                                0.005070839320274
                                0.003965449234824
                                0.005141575516457
                                0.008095985681670
                                0.001483700849618
                                0.005567576036766
                                0.005577049030324
                                0.004903086137207
                                0.001203802308956
                                0.000865378260807
                                0.007117466045659
                                0.004836612788125
                                0.001459382321869
                                0.001205863361697
                                0.001285303885675
                                0.000647384379762
                                0.000464598909204
                                0.000399668304787
                                0.005333687825816
                                0.000949214253796
                                0.006029370939877
                                0.005794494831027
                                0.000246983947902
                                0.000275642459985
                                0.001058372911851
                                0.001198060321575
                                0.000264526578687
                                0.000263519734800
                                0.000201413435748
                                0.000264668673590
                                0.000336444192495
                                0.003069114584354
                                0.000283394075285
                                0.000160852783902
                                0.000283713450496
                                0.049577317771898
                                0.000035882752299
                                0.000020721767423
                                0.000009376964469
                                0.000044598718343
                        C ***************************************************************
                        C Tallies
                        f06:n 10                               $ Energy deposition in cell 10 for E [MeV/g] (dose)
                        f16:e 10
                        f26:h 10
                        f4:n 7
                        C ***************************************************************
                        MODE N P E H D T S A #
                        IMP:N 1 3r 0 2 4r
                        IMP:P 1 3r 0 1 4r
                        IMP:E 1 3r 0 1 4r
                        IMP:H 1 3r 0 1 4r
                        IMP:D 1 3r 0 1 4r
                        IMP:T 1 3r 0 1 4r
                        IMP:S 1 3r 0 1 4r
                        IMP:A 1 3r 0 1 4r
                        IMP:# 1 3r 0 1 4r                        
                        C ***************************************************************
                        C Tallies
                        CUT:N j 0.000000010 $kill neutrons below 10 µeV
                        CUT:E j 0.050 $Kill electrons below 50 KeV
                        CUT:P j 0.003 $Kill photons below 3 KeV
                        c PHYS:P 100.0 0.1 $max sigma table energy; analog capture below 100 keV
                        PRINT 110
                        nps 10E6 $Number of particles
                        prdmp 2j 1 1 10E12 $Print and dump card; PRDMP NDP NDM MCT NDMP DMMP with 1 for writing tallies for plotting
                        C ***************************************************************
                        fmesh34:n geom=xyz origin= -5 0 -2
                                        imesh=53 iints=99
                                        jmesh=9 jints=30
                                        kmesh=2 kints=15
                        '''

    def runMCNP(self, gray, plot, DATAPATH):

        # Set environment variables
        os.environ['DATAPATH'] = DATAPATH
        values = MCNP.setDensityValues(self, d_0, d_f)
        logging.info("DATAPATH variable set to " + DATAPATH)
        # Change working dir to output_nps10E7 for file creation purposes
        os.chdir(OUTPUT)
        logging.warning("Working directory changed to " + OUTPUT)

        for d in values:
            density = str(d)
            mcnp = MCNP(density)
            input_file = mcnp.get_input_file()

            file = open(INPUT_FILE_NAME, 'w')
            file.write(input_file)
            file.close()

            mcnp.format_input_file()

            os.system("mpiexec -np 96 mcnp6.mpi i = " + INPUT_FILE_NAME)
            datanames.append(q.get())

        tallies = mcnp.getTallies(INPUT_FILE_NAME)
        nps = mcnp.getNPS()
        analyzer = Analyzer(datanames, gray, plot, tallies, nps, values)
        analyzer.analyze()
        os.chdir("..")
        logging.warning("Working directory changed back to root")
        logging.warning("----- END OF THE SCRIPT -----")

    def setDensityValues(self, d_0, d_f):
        step = (d_f-d_0)/25
        values = np.arange(d_0, d_f, step)

        if len(values) > 25:
            logging.warning("Density vector contains more values than MCNP can handle.")
            sys.exit()

        return values
    def getNPS(self):
        it = iter(open(INPUT_FILE_NAME))
        nps = 0
        for lines in it:
            if "nps" in lines:
                nps = lines.split(" ")[1]
        return nps
    def getTallies(self, input_file_name):

        it = iter(open(input_file_name))
        n = ["f1", "f2", "f4", "f5a", "fip5", "fir5", "fic5",  "f6", "+f6", "f7", "f8", "+f8"]
        tallies = []
        for lines in it:

            if any(item in lines for item in n):

                tallies.append(re.split(' |:', lines)[0])

        return tallies
    def get_input_file(self):
        return self.input_file

    def format_input_file(self):
        formatted_input = ''
        f0 = open(INPUT_FILE_NAME)
        n = 0
        for line in f0:
            n += 1
            if n == 1:
                formatted_input += line.strip() + "\n"
            elif n > 1:
                formatted_input += line[24:]
                if len(line[24:]) == 0:
                    formatted_input += "\n"

        with open(INPUT_FILE_NAME, 'w') as f:
            f.write(formatted_input)

        f.close()
        f0.close()

