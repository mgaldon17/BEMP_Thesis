
%Reshape vectors
FX = reshape(FX.',[],1);
FY_156 = reshape(FY_76.',[],1);
err_156 = reshape(err_76.',[],1);
FY_166 = reshape(FY_106.',[],1);
err_166 = reshape(err_106.',[],1);
gray = true;
errors = true;

%Check if FX and FY and err lengths match
[FY_1,err_1] = checkLengths(FX,FY_156, err_156);
[FY_2,err_2] = checkLengths(FX,FY_166, err_166);

%Convert MeV/g into Gy (1Gy=1J/Kg)
convertIntoGray(FY_1, err_1, gray);
convertIntoGray(FY_2, err_2, gray);

%Plot


plot(FX, FY_1, 'r') %F76
hold on
plot(FX, FY_2, 'b') %F176
hold on
title('Linear plot of E with 2x2 planar source in (3, 2.3, 0)')
checkIfGray(gray)
if errors == true
    errorbar(FX,FY_1,err_1.*FY_1, 'r', 'HandleVisibility','off')
    errorbar(FX,FY_2,err_2.*FY_2, 'b', 'HandleVisibility','off')
end
hold off
legend('F76', 'F106')


