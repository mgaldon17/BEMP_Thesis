
%Reshape vectors
FX = reshape(FX.',[],1);
FY_156 = reshape(FY_156.',[],1);
err_156 = reshape(err_156.',[],1);
%FY_166 = reshape(FY_166.',[],1);
%err_166 = reshape(err_166.',[],1);
gray = true;
errors = true;

%Check if FX and FY and err lengths match
[FY_1,err_1] = checkLengths(FX,FY_156, err_156);
%[FY_2,err_2] = checkLengths(FX,FY_166, err_166);

%Convert MeV/g into Gy (1Gy=1J/Kg)
convertIntoGray(FY_1, err_1, gray);
%convertIntoGray(FY_2, err_2, gray);

%Plot


plot(FX, FY_1, 'r')
hold on
%plot(FX, FY_2, 'b')
title('Linear plot of secondary electrons in water')
checkIfGray(gray)
if errors == true
    errorbar(FX,FY_1,err_1.*FY_1, 'r', 'HandleVisibility','off')
    %errorbar(FX,FY_2,err_2.*FY_2, 'b', 'HandleVisibility','off')
end
hold off
%legend('F156', 'F166')


