
%Reshape vectors
FX = reshape(F56_X.',1,[]);
FY = reshape(F74Y_E.',1, []);

%Check if lengths match
if length(FX) ~= length(FY)
    fprintf("\nCorrecting length of vectors...\n")
    while length(FX)<length(FY)
        FY(:,1)=[];
    end

    fprintf("Length FX: %d\n", length(FX))
    fprintf("Length FY: %d\n", length(FY))
else
    

end


%Plot

%For Tally x6
semilogy(FX,FY)
xlabel("Energy (MeV)"), ylabel("Flux (MeV/cm2)")
grid