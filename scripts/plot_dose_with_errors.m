
%Reshape vectors
FX = reshape(FX.',[],1);
FY = reshape(FY_76.',[],1);
err = reshape(err.',[],1);
gray = true;
errors = true;

%Check if FX and FY and err lengths match
[FY,err] = checkLengths(FX,FY, err);

%Convert MeV/g into Gy (1Gy=1J/Kg)
convertIntoGray(FY, err, gray);


%Plot

%For Tally 6

tally = "F76";

plot(FX, FY)

if errors == true
    errorbar(FX,FY,err.*FY)
end

title('Linear plot ' + tally + ' in water')
checkIfGray(gray)
grid
