#!/usr/bin/perl
# @file main.pl
# @author lihuax
# @version 1.0
# @description
#################

# 输入和输出文件名
my $input_file = 'summary.csv';
my $output_file = 'output_table.txt';

# 打开输入和输出文件
open my $input_fh, '<', $input_file or die "无法打开输入文件 $input_file: $!";
open my $output_fh, '>', $output_file or die "无法打开输出文件 $output_file: $!";

# 开始LaTeX文档
print $output_fh "\\documentclass{article}\n";
print $output_fh "\\usepackage{longtable}\n";
print $output_fh "\\usepackage{graphicx}\n";
print $output_fh "\\usepackage{booktabs}\n";
print $output_fh "\\begin{document}\n";

# 开始longtable环境
print $output_fh "\\begin{longtable}{cccccc}\n";
print $output_fh "\\caption{Your Table Caption} \\\\\n";
print $output_fh "\\toprule\n";
print $output_fh "File & Lane \\# & MW & RepeatNum & HomoOrHeter \\\\\n";
print $output_fh "\\midrule\n";

# 处理每一行数据
while (<$input_fh>) {
    chomp;
    # 将路径中的斜杠 / 替换为 LaTeX 中的路径斜杠 \
    s/\.\.\/data\//..\\data\\/g;
    my @fields = split /,/;
    # 将数组中的元素用 & 连接，并在末尾添加 \\
    print $output_fh join(' & ', @fields), " \\\\\n";
}

# 结束longtable环境
print $output_fh "\\bottomrule\n";
print $output_fh "\\end{longtable}\n";

# 结束LaTeX文档
print $output_fh "\\end{document}\n";

# 关闭文件句柄
close $input_fh;
close $output_fh;

print "转换完成，结果保存在$output_file中。\n";
