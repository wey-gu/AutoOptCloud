notice("cloud_pipeline: applying conf changes")

$metrics_weight = "1.0"
$io_ops_weight_multiplier = "1.0"
$ram_weight_multiplier = "%w_ram"
$disk_weight_multiplier = "%w_disk"
$user_p = "%w_user_p"
$iowait_p = "%w_iowait_p"
$frequency = "%w_frequency"
$idle_p = "%w_idle_p"
$cpu_p = "%w_cpu_p"
$kernel_p = "%w_kernel_p"
$weight_setting = "cpu.user.percent=${user_p}, cpu.iowait.percent=${iowait_p}, cpu.frequency=${frequency}, cpu.idle.percent=${idle_p}, cpu.percent=${cpu_p}, cpu.kernel.percent=${kernel_p}"
nova_config{
  "DEFAULT/io_ops_weight_multiplier":   value => $io_ops_weight_multiplier;
  "DEFAULT/ram_weight_multiplier":      value => $ram_weight_multiplier;
  "DEFAULT/disk_weight_multiplier":     value => $disk_weight_multiplier;
  "metrics/weight_multiplier":          value => $metrics_weight;
  "metrics/weight_setting":             value => $weight_setting;
}
exec {"restart nova-scheduler service":
  command => "/usr/sbin/service nova-scheduler restart"
}
exec {"wait for nova-scheduler":
  command => "sleep 30",
  path => "/usr/bin:/bin",
}
