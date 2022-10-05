
%Reshape vectors
FX = reshape(FX.',[],1);
FY = reshape(F6Y_P.',[],1);
err = reshape(F6Y_P_err.',[],1);
gray = true;
errors = true;

%Check if FX and FY and err lengths match
[FY,err] = checkLengths(FX,FY, err);

%Convert MeV/g into Gy (1Gy=1J/Kg)
convertIntoGray(FY, err, gray);


%Plot

%For Tally 6

tally = "6+ for cell 5";

plot(FX, FY)

if errors == true
    errorbar(FX,FY,err.*FY)
end

title('Linear plot ' + tally + ' in Polyethilene')
checkIfGray(gray)
grid
