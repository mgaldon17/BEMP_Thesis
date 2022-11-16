function [FY,err] = convertIntoGray(FY, err, gray)
%Convert dose in MeV/g into gray
conversion = 6.24E9 ; %1 gray in MeV/g is 6.24E9 
    if gray == true
        for i=1:length(FY)
            FY(i)=FY(i)./conversion;
            err(i)=err(i)./conversion;
        end
    
    end
end

