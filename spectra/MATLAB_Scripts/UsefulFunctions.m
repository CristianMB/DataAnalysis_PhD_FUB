classdef UsefulFunctions
    
   methods (Static)
   
   %% KATAURA PLOT VALUES CALCULATION

    function [nuRBM,w11, w22, w33, w44,diam,theta, type]=CalculateKataura(P)
    % Calculate RBM frequency, energy transitions (in nm scale), diameter, chiral angle and type of nanotube for chirality [n,m]. Based on Bachilo (2002) and Araujo (2010)

    n=P(1);
    m=P(2);

    %Bachilo: https://www.science.org/doi/10.1126/science.1078727
    dcc = 0.144;        %nm Carbon carbon distance
    % Surfacntant environment
    A = 223.5;          %cm-1
    B = 12.5;           %cm-1
    % Free standing environment
%     A = 248;          %cm-1
%     B = 0;           %cm-1    

    diam= dcc*sqrt(3)*(sqrt(n.^2+m.^2+n.*m))/pi;
    theta=atan(sqrt(3)*m./(m+2*n));
    nuRBM=(A./diam)+B ;
    
    %Araujo: https://www.sciencedirect.com/science/article/pii/S1386947710000445
    a=1.049;            %eV nm
    b=0.456;
    c=0.812;            %nm-1
    hc = 1240.84193;    %h*c value to convert energy to nm
    
    
    if mod(n-m,3)==0 % METALLIC TUBES using Araujo Equations
        type = 'M';

        %M11 Araujo, two branches
        e1a=((a*3./diam).*(1+(b*log10(c./(3./diam)))))-0.19*cos(3*theta)./diam^2;    %(in eV)
        e1b=((a*3./diam).*(1+(b*log10(c./(3./diam)))))+0.29*cos(3*theta)./diam^2;    %(in eV)
        w11=hc/e1a;                                                                 %(in nm)
        w22=hc/e1b;                                                                 %(in nm)

        %M22 Araujo, two branches
        e2a=((a*6./diam).*(1+(b*log10(c./(6./diam)))))-0.60*cos(3*theta)./diam^2;    %(in eV)
        e2b=((a*6./diam).*(1+(b*log10(c./(6./diam)))))+0.57*cos(3*theta)./diam^2;    %(in eV)
        w33=hc/e2a;                                                                 %(in nm)
        w44=hc/e2b;                                                                 %(in nm)

    end
       
    if mod(n-m,3)==1 % SEMICONDUCTING TUBES using Bachilo Equations and Araujo Equations
       type = 'S';

       %S11 and S22 Bachilo with (m-n)%3 = 1
        nu11=(1*10^7)./(157.5+1066.9*diam)- 710*cos(3*theta)./diam.^2;              %(in cm-1)
        nu22=(1*10^7)./(145.6+ 575.7*diam)+1375*cos(3*theta)./diam.^2;              %(in cm-1)
        w11=(1*10^7)./nu11;                                                         %(in nm)
        w22=(1*10^7)./nu22;                                                         %(in nm)

        %S33 and S44 Araujo (p=4,5) lower33 (4), upper44 (5)
        e33=((a*4/diam).*(1+(b*log10(c./(4./diam)))))-0.42*cos(3*theta)./diam^2 +(0.0596*4/diam); %(in eV)
        e44=((a*5/diam).*(1+(b*log10(c./(5./diam)))))+0.40*cos(3*theta)./diam^2 +(0.0596*5/diam); %(in eV)
        w33=hc/e33;
        w44=hc/e44;
    end
       
    if mod(n-m,3)==2 % SEMICONDUCTING TUBES using Bachilo Equations and Araujo Equations
       type = 'S';

       %S11 and S22 Bachilo with (m-n)%3 = 2
        nu11=(1*10^7)./(157.5+1066.9*diam)+ 369*cos(3*theta)./diam.^2;      %(in cm-1)
        nu22=(1*10^7)./(145.6+ 575.7*diam)-1475*cos(3*theta)./diam.^2;      %(in cm-1)
        w11=(1*10^7)./nu11;                                                %(in nm)
        w22=(1*10^7)./nu22;                                                %(in nm)

        %S33 and S44 Araujo (p=4,5) upper33 (4), lower44 (5) + term
        %added for all beyond M11
        e33=((a*4/diam).*(1+(b*log10(c./(4./diam)))))+0.42*cos(3*theta)/diam^2+(0.0596*4/diam);  %(in eV)
        e44=((a*5/diam).*(1+(b*log10(c./(5./diam)))))-0.40*cos(3*theta)/diam^2+(0.0596*5/diam);   %(in eV)
        w33=hc/e33;                                                       %(in nm)
        w44=hc/e44;                                                       %(in nm)
    end
    end

 
    
    %% RAMAN MEASUREMENTS FUNCTIONS - UAntwerp
    
    function dataStructures = ReadXploraFromPaths(paths, NDel)
    % Read an individual Raman spectrum file, perform multimedian filtering and return a structure containing X (Raman shift),P (Pixel positions),Y values(Intensity)

        dataStructures = struct();  
        for p = 1:length(paths)
            try
                dataset_name = strsplit(paths{p}, "\");
                fieldName = ['DATA_', strrep(dataset_name{end-1}, '.', '')];
                dirInfo = dir(fullfile(paths{p}, '*.m3d'));
                fileList = {dirInfo(~[dirInfo.isdir]).name};
                structure = struct();

                for f = 1:length(fileList)
                    raw_spectrum = RdExp([paths{p},fileList{f}]);
                    raw_spectrum(:,2)=[];
                    NumSpec=length(raw_spectrum(1,:))-1;
                    NumDel=NDel;
                    X=raw_spectrum(:,1);
                    for i=1:1024
                        spectrum=sort(raw_spectrum(i,2:NumSpec+1));
                        Y(:,i)= mean(spectrum(NumDel+1:NumSpec-NumDel));  
                    end
                    sampleName = upper(strrep(fileList{f}, '.m3d',''));

                    structure.(sampleName).X = X;
                    structure.(sampleName).Y = Y';
                    structure.(sampleName).N = sampleName;
                    structure.(sampleName).P = (1:1024)';
                    
                end 
               dataStructures.(fieldName) = structure;
               assignin('caller', fieldName, structure); % Assign data to a variable in the caller workspace

            catch ME
                % Print the path that caused the error
                disp(['Error reading data from path: ' paths{p}]);
                % Re-throw the error
                rethrow(ME);
            end
        end       
    end     
    function plotRaman(SamplesToPlot, offset, wl)
        % Create a figure for the plot
        figure;

        % Get a ColorBrewer colormap (e.g., 'Set1', 'Dark2', etc.)
        numSamples = length(SamplesToPlot);  % Number of samples to plot
        for sampleIdx = 1:numSamples
            currentSample = SamplesToPlot{sampleIdx};

            % Get the current sample, X values, and Y values
            currentX = currentSample.X;
            currentY = currentSample.Y - offset * sampleIdx;
            currentN = currentSample.N;

            % Plot each sample using a different color from the colormap
            plot(currentX, currentY, 'DisplayName', currentN, 'LineWidth', 1.3);
            hold on;  % Add spectra to the same plot
        end

        % Add labels and legend
        xlabel('Raman Shift (cm^{-1})', 'FontSize', 14);
        ylabel('Normalized Intensity (a.u.)', 'FontSize', 14);
        % Conditional title based on wavelength parameter 'wl'
        if nargin < 3 || isempty(wl)
            title('Raman Spectra');
        else
            title(['Raman spectra at ', num2str(wl), ' nm']);
        end
            % Show legend with proper font size
        legend('show', 'FontSize', 11);

        % Optional: Customize the plot further if needed
        grid on;

        % Hold off to stop adding new plots to the current figure
        hold off;
    end

    
    
   %% ABSORPTION MEASUREMENTS FUNCTIONS
    
    function samples = readSamplesData(filePath)
        % Read the header
        header = readcell(filePath, 'Range', 'A1:ZZ1');
        header = cellfun(@(x) strrep(x, ' 100%T', ''), header, 'UniformOutput', false);
        sampleNames = header(1, 1:2:end);
        warning('off', 'MATLAB:strrep:InvalidInputType');
        % Read ONLY the datalines
        data = readmatrix(filePath, 'Range', ['A' num2str(3) ':ZZ' num2str(3000)]);

        samples = struct();

        % Iterate through each sample and store wavelength and absorption data
        for i = 1:length(sampleNames)
            % Extract wavelength and absorption data for the current sample
            wavelengths = data(:, 2*i - 1); % Odd columns contain wavelength
            absorption = data(:, 2*i);       % Even columns contain absorption
            warning('off', 'MATLAB:strrep:InvalidInputType');
            % Store the data in the container object with the sample name
            sampleName = strrep(sampleNames{i}, '-', '_');
            samples.(sampleName).X = wavelengths;
            samples.(sampleName).Y = absorption;
            samples.(sampleName).N = sampleName;
        end
    end
    function dataStructures = ReadAbsorptionFromPaths(paths)
        dataStructures = struct();
        for i = 1:length(paths)
            % Extract the suffix from the path
            try
                % Extract the suffix from the path variable
                dataset_name = strsplit(paths{i}, "\");
                % Create dynamic field name for the structure
                fieldName = ['DATA_', strrep(dataset_name{5}, '.csv', '')];
                % Read the data from the current path
                data = UsefulFunctions.readSamplesData(paths{i});
                
                structure = struct(fieldName, data);
                
                % Check if the field already exists
                if isfield(dataStructures, fieldName)
                    dataStructures.(fieldName) = UsefulFunctions.mergeStructures(dataStructures.(fieldName), data);
                else
                    dataStructures.(fieldName) = structure.(fieldName);        
                end
                
                % Assign data to a variable in the caller workspace
                assignin('caller', fieldName, dataStructures.(fieldName)); 
                
            catch ME
                % Print the path that caused the error
                disp(['Error reading data from path: ' paths{i}]);
                % Re-throw the error
                rethrow(ME);
            end
        end
    end
    function plotAbsorption(SamplesToPlot, offset)
        % Create a figure for the plot
        figure;
        
        for sampleIdx = 1:length(SamplesToPlot)
            currentSample = SamplesToPlot{sampleIdx};
                % Get the current sample, X values, and Y values
                currentX = currentSample.X;
                currentY = currentSample.Y - offset*sampleIdx;
                currentN = currentSample.N;
                plot(currentX, currentY, 'DisplayName', currentN,'LineWidth', 1.3);
                hold on; % Add spectra to the same plot
        end

        % Add labels and legend
        xlabel('Wavelength (nm)', 'FontSize', 14);
        ylabel('Normalized Absorption (a.u.)', 'FontSize', 14);
        title('Absorption Spectra','FontSize', 14);
        legend('show','FontSize', 11);
        % Optional: Customize the plot further if needed
        grid on;
        % Hold off to stop adding new plots to the current figure
        hold off;

    end
 
      
   end
  
end