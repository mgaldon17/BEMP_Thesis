function [FY,err] = checkLengths(FX,FY,err)

    %Check if lengths match
    if length(FX) ~= length(FY)
        fprintf("\nCorrecting length of vectors...\n")
        while length(FX)<length(FY)
            FY(end)=[];
            err(end)=[];
        end
    
        fprintf("Length FX: %d\n", length(FX))
        fprintf("Length FY: %d\n", length(FY))
    else

    end
end

