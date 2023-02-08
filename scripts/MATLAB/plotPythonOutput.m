
%In this script we have to load the workspace manually taking the vectors
%from the txt output files from Python
x = [0.0005, 0.00058, 0.00066, 0.00074, 0.00082, 0.0009, 0.00098, 0.00106, 0.00114, 0.00122, 0.0013, 0.00138, 0.00146, 0.00154, 0.00162, 0.0017, 0.00178, 0.00186, 0.00194, 0.00202, 0.0021, 0.00218, 0.00226, 0.00234, 0.00242];
[FY_05,err_05] = convertIntoGray(y_05, y_err_05, true);
[FY_1,err_1] = convertIntoGray(y_1, y_err_1, true);
[FY_15,err_15] = convertIntoGray(y_15, y_err_15, true);
[FY_2,err_2] = convertIntoGray(y_2, y_err_2, true);
[FY_3,err_3] = convertIntoGray(y_3, y_err_3, true);
plot(x, FY_05, x, FY_1, x, FY_15, x, FY_2, x, FY_3)
hold on 
legend('0.5 %','1 %','1.5 %','2 %', '3 %')
xlabel("Density g/cm3")
ylabel("Dose (Gray)")
title("Electron F6") %Edit this line for tally type
save("electron.mat") %save