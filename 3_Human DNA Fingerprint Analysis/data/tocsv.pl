#!/usr/bin/perl
# @file main.pl
# @author lihuax
# @version 1.0
# @description
#################

use 5.010;
use strict;
use warnings;

# 获取当前文件夹下的所有txt文件
my @txt_files = glob("*.txt");

# 处理每个txt文件
foreach my $txt_file (@txt_files) {
    my $csv_file = $txt_file;
    $csv_file =~ s/\.txt$/\.csv/;

    open my $input_fh, '<', $txt_file or die "无法打开文件 $txt_file: $!";
    open my $output_fh, '>', $csv_file or die "无法创建文件 $csv_file: $!";

    # 跳过第一行
    <$input_fh>;

    # 写入CSV文件的标题行
    print $output_fh "Lane #, Band #, Peak Rf, Peak value, Raw volume, Cal. volume, MW\n";

    # 读取每一行，进行处理并写入CSV文件
    while (<$input_fh>) {
        chomp;
        next if /^\s*$/;  # 跳过空行

        # 提取数据并写入CSV文件
        my ($lane, $band, $peak_rf, $peak_value, $raw_volume, $cal_volume, $mw) = split;
        print $output_fh "$lane, $band, $peak_rf, $peak_value, $raw_volume, $cal_volume, $mw\n";
    }

    close $input_fh;
    close $output_fh;

    print "已将文件 $txt_file 转换为 $csv_file\n";
}

