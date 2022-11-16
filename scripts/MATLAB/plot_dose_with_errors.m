
%Reshape vectors
FX = reshape(FX.',[],1);
FY = reshape(FY_166.',[],1);
err = reshape(err_166.',[],1);
gray = true;
errors = true;

%Check if FX and FY and err lengths match
[FY,err] = checkLengths(FX,FY, err);

%Convert MeV/g into Gy (1Gy=1J/Kg)
convertIntoGray(FY, err, gray);


%Plot

%For Tally 6

tally = "F156";

plot(FX, FY)
legend()
if errors == true
    errorbar(FX,FY,err.*FY)
end

title('Linear plot ' + tally + ' in water')
checkIfGray(gray)
grid
hold on
