resource "signalfx_detector" "cpu_high" {
  name        = "High CPU Usage Detector"
  description = "Alert when CPU usage is high"
  severity    = "Critical"

  program_text = <<EOF
A = data('cpu.utilization').publish(label='CPU')
detect(when(A > 80)).publish('High CPU')
EOF
}