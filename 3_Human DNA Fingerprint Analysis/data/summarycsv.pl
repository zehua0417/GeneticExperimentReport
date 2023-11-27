#!/usr/bin/perl
# @file main.pl
# @author lihuax
# @version 1.0
# @description
#################

use 5.010;
use strict;
use warnings;

# 获取当前文件夹下的所有csv文件
my @csv_files = glob("*.csv");
my $output_file = "summary.csv"; # 添加双引号并在文件名前添加分号
open my $output_fh, '>', $output_file or die "cannot create file $output_file: $?";
print $output_fh "Lane #, Band #, Peak Rf, Peak value, Raw volume, Cal. volume, MW\n";

foreach my $csv_file (@csv_files) {
    open my $input_fh, '<', $csv_file or die "cannot open file $csv_file: $!";
    <$input_fh>;
    while (<$input_fh>) {
        chomp;
        next if /^\s*$/;  # 跳过空行

        # 提取数据并写入CSV文件
        my ($lane, $band, $peak_rf, $peak_value, $raw_volume, $cal_volume, $mw) = split /,\s*/;
        print $output_fh "$lane, $band, $peak_rf, $peak_value, $raw_volume, $cal_volume, $mw\n";
    }
    close $input_fh;
}
close $output_fh;
say "summary success"; # 使用 say 函数来输出文本，并添加分号

