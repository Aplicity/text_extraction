clear all
clc

text = fileread('test.txt');
index_Keyword = strfind(text,'LETTER OF CREDIT AND REIMBURSEMENT AGREEMENT');
index_Table = strfind(lower(text),lower('Table of Contents'));

final_Keyword = 0;
final_Table = 0;
temp_distance = inf;
for k_1=1:length(index_Keyword)
    for k_2 = 1:length(index_Table)
        distance = index_Table(k_2) - index_Keyword(k_1);
        if distance > 0
            if distance < temp_distance
                final_Keyword = index_Keyword(k_1);
                final_table = index_Table(k_2);
                temp_distance = distance;
            end
        end
    end
end


text2=text(final_Keyword:end);

fid = fopen('text2.txt', 'wt');
fprintf(fid, '%s\n', text2);
fclose(fid);
% save('text2.txt','text2','-append')