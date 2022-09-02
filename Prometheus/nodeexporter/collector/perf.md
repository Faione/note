## PerfCollector

node exporter中，通过perf获取数据的collector模块，默认关闭，通过`--collector.perf`启动，对于一些系统，需要通过设置`kernel.perf_event_paranoid`值小于1

```shell
$ sysctl -w kernel.perf_event_paranoid=X
# 2 allow only user-space measurements (default since Linux 4.6).
# 1 allow both kernel and user measurements (default before Linux 4.6).
# 0 allow access to CPU-specific data but not raw tracepoint samples.
# -1 no restrictions.
```

perf collector中定义了 perf collector 与 perf TracepointCollector，后者通过追加`--collector.perf.tracepoint`进行启动

```go
type perfCollector struct {
	hwProfilerCPUMap    map[*perf.HardwareProfiler]int
	swProfilerCPUMap    map[*perf.SoftwareProfiler]int
	cacheProfilerCPUMap map[*perf.CacheProfiler]int
	perfHwProfilers     map[int]*perf.HardwareProfiler
	perfSwProfilers     map[int]*perf.SoftwareProfiler
	perfCacheProfilers  map[int]*perf.CacheProfiler
	desc                map[string]*prometheus.Desc
	logger              log.Logger
	tracepointCollector *perfTracepointCollector
}

type perfTracepointCollector struct {
	// desc is the mapping of subsystem to tracepoint *prometheus.Desc.
	descs map[string]map[string]*prometheus.Desc
	// collection order is the sorted configured collection order of the profiler.
	collectionOrder []string

	logger    log.Logger
	profilers map[int]perf.GroupProfiler
}
```

### Perf Collector

`perfCollector`数据结构中涉及 perfHwProfiler、perfSwProfiler、perfCacheProfiler 三个profiler，并通过CpuMap将这些数据与对应的CPU进行关联。从名字中可以看出，perfCollector监控指标来源perf中的`Hardware event`, `Software event`, `Hardware cache event`三类事件

HardwareProfile中监控指标如下

```go
type HardwareProfile struct {
	CPUCycles             *uint64 `json:"cpu_cycles,omitempty"`
	Instructions          *uint64 `json:"instructions,omitempty"`
	CacheRefs             *uint64 `json:"cache_refs,omitempty"`
	CacheMisses           *uint64 `json:"cache_misses,omitempty"`
	BranchInstr           *uint64 `json:"branch_instr,omitempty"`
	BranchMisses          *uint64 `json:"branch_misses,omitempty"`
	BusCycles             *uint64 `json:"bus_cycles,omitempty"`
	StalledCyclesFrontend *uint64 `json:"stalled_cycles_frontend,omitempty"`
	StalledCyclesBackend  *uint64 `json:"stalled_cycles_backend,omitempty"`
	RefCPUCycles          *uint64 `json:"ref_cpu_cycles,omitempty"`
	TimeEnabled           *uint64 `json:"time_enabled,omitempty"`
	TimeRunning           *uint64 `json:"time_running,omitempty"`
}
```
SoftwareProfile中监控指标如下

```go
type SoftwareProfile struct {
	CPUClock        *uint64 `json:"cpu_clock,omitempty"`
	TaskClock       *uint64 `json:"task_clock,omitempty"`
	PageFaults      *uint64 `json:"page_faults,omitempty"`
	ContextSwitches *uint64 `json:"context_switches,omitempty"`
	CPUMigrations   *uint64 `json:"cpu_migrations,omitempty"`
	MinorPageFaults *uint64 `json:"minor_page_faults,omitempty"`
	MajorPageFaults *uint64 `json:"major_page_faults,omitempty"`
	AlignmentFaults *uint64 `json:"alignment_faults,omitempty"`
	EmulationFaults *uint64 `json:"emulation_faults,omitempty"`
	TimeEnabled     *uint64 `json:"time_enabled,omitempty"`
	TimeRunning     *uint64 `json:"time_running,omitempty"`
}
```
CacheProfile中监控指标如下

```go
type CacheProfile struct {
	L1DataReadHit      *uint64 `json:"l1_data_read_hit,omitempty"`
	L1DataReadMiss     *uint64 `json:"l1_data_read_miss,omitempty"`
	L1DataWriteHit     *uint64 `json:"l1_data_write_hit,omitempty"`
	L1InstrReadMiss    *uint64 `json:"l1_instr_read_miss,omitempty"`
	LastLevelReadHit   *uint64 `json:"last_level_read_hit,omitempty"`
	LastLevelReadMiss  *uint64 `json:"last_level_read_miss,omitempty"`
	LastLevelWriteHit  *uint64 `json:"last_level_write_hit,omitempty"`
	LastLevelWriteMiss *uint64 `json:"last_level_write_miss,omitempty"`
	DataTLBReadHit     *uint64 `json:"data_tlb_read_hit,omitempty"`
	DataTLBReadMiss    *uint64 `json:"data_tlb_read_miss,omitempty"`
	DataTLBWriteHit    *uint64 `json:"data_tlb_write_hit,omitempty"`
	DataTLBWriteMiss   *uint64 `json:"data_tlb_write_miss,omitempty"`
	InstrTLBReadHit    *uint64 `json:"instr_tlb_read_hit,omitempty"`
	InstrTLBReadMiss   *uint64 `json:"instr_tlb_read_miss,omitempty"`
	BPUReadHit         *uint64 `json:"bpu_read_hit,omitempty"`
	BPUReadMiss        *uint64 `json:"bpu_read_miss,omitempty"`
	NodeReadHit        *uint64 `json:"node_read_hit,omitempty"`
	NodeReadMiss       *uint64 `json:"node_read_miss,omitempty"`
	NodeWriteHit       *uint64 `json:"node_write_hit,omitempty"`
	NodeWriteMiss      *uint64 `json:"node_write_miss,omitempty"`
	TimeEnabled        *uint64 `json:"time_enabled,omitempty"`
	TimeRunning        *uint64 `json:"time_running,omitempty"`
}
```

