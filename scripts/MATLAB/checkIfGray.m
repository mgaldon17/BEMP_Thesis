function [] = checkIfGray(gray)
%CHECKIFGRAY Summary of this function goes here
%   Detailed explanation goes here

if gray ==true
    ylabel("Dose (gray)")
    else
        ylabel("Dose (MeV/g)")
end
xlabel("Energy (J)")

end

