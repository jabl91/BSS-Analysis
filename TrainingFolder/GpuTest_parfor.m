
%Training code for parallalel computing.
%Clear all the previous "mess"
    clear all;
    clc;
    g= gpuDevice(1);
    reset(g);


%Uncomment to get all possible methods of a GpuArray.
    %methods('gpuArray');

%Single Core Code

    % tic
    % n = 200;
    % A = 500;
    % a = zeros(n);
    % for i = 1:n
    %     a(i) = max(abs(eig(rand(A))));
    % end
    % toc


%Several Cores Code


    % 
    % tic
    % ticBytes(gcp);
    % n = 200;
    % A = 500;
    % a = zeros(n);
    % parfor i = 1:n
    %     a(i) = max(abs(eig(rand(A))));
    % end
    % tocBytes(gcp)
    % toc


%Example for user-functions running on GPU.

    % tic
    % meas = ones(1000)*3; % 1000-by-1000 matrix
    % gn   = rand(1000,'gpuArray')/100 + 0.995;
    % %gn   = rand(1000)/100 + 0.995;
    % offs = rand(1000,'gpuArray')/50  - 0.01;
    % %offs = rand(1000)/50  - 0.01;
    % 
    % corrected = arrayfun(@myCal,meas,gn,offs);
    % 
    % results = gather(corrected);
    % toc
    
%Another example where a random number is multiplied in the GPU

    % G = 2*ones(4,4,'gpuArray')
    % H = arrayfun(@myfun, G)
    
%When more than 2 dimensions are used (pages of an array)

    M = 300;       % output number of rows
    K = 500;       % matrix multiply inner dimension
    N = 1000;      % output number of columns
    P = 200;       % number of pages
    A = rand(M,K,'gpuArray');   
    B = rand(K,N,P,'gpuArray');
    C = pagefun(@mtimes,A,B);
    s = size(C)    % returns M-by-N-by-P 
    
