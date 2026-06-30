const YUANLI_DEFAULT_DATA = {
  appleHealth: {
    range: { start: '—', end: '—', days: 0 },
    dataQuality: {},
    metrics: {},
    thresholdCounts: {},
    workouts: []
  },
  clinicalBaseline: {},
  agentScores: {},
  nextProtocol: {}
};

function n(value, fallback = 0) {
  return Number.isFinite(Number(value)) ? Number(value) : fallback;
}

function fmt(value, digits = 0, fallback = '—') {
  if (value === null || value === undefined || value === '') return fallback;
  const num = Number(value);
  if (!Number.isFinite(num)) return fallback;
  return num.toLocaleString('zh-CN', { maximumFractionDigits: digits, minimumFractionDigits: digits });
}

function pct(value, target) {
  if (!target) return 0;
  return Math.max(0, Math.min(100, Math.round((n(value) / target) * 100)));
}

function qualityLabel(status) {
  const s = String(status || '').toLowerCase();
  if (s.includes('good')) return { text: '可用', cls: 'good' };
  if (s.includes('partial') || s.includes('medium')) return { text: '部分可用', cls: 'warn' };
  if (s.includes('missing') || s.includes('insufficient') || s.includes('weak')) return { text: '不足', cls: 'bad' };
  return { text: '待接入', cls: 'warn' };
}

function movementScore(data) {
  const steps = data.appleHealth?.metrics?.steps || {};
  const avg = n(steps.avg);
  const floorScore = Math.min(100, Math.round(avg / 80));
  const trendPenalty = n(steps.last30Avg) < n(steps.first30Avg) ? 10 : 0;
  return Math.max(0, floorScore - trendPenalty);
}

function zone2Score(data) {
  const workouts = data.appleHealth?.workouts || [];
  const exercise = data.appleHealth?.metrics?.exerciseMinutes || {};
  const days30 = n(exercise.last30Avg) >= 20 ? 40 : n(exercise.last30Avg) >= 10 ? 25 : 12;
  const hasWorkout = workouts.length ? 15 : 0;
  return Math.min(100, days30 + hasWorkout);
}

function sleepScore(data) {
  const sleep = data.appleHealth?.metrics?.sleepDurationHours || {};
  const days = n(sleep.days);
  if (days < 5) return 20;
  return Math.min(100, Math.round(n(sleep.avg) / 7.5 * 100));
}

function recoveryScore(data) {
  const rhr = data.appleHealth?.metrics?.restingHeartRate || {};
  const hrv = data.appleHealth?.metrics?.hrvMs || {};
  let score = 60;
  if (n(rhr.last30Avg) && n(rhr.first30Avg) && n(rhr.last30Avg) < n(rhr.first30Avg)) score += 12;
  if (n(hrv.last30Avg) && n(hrv.first30Avg) && n(hrv.last30Avg) > n(hrv.first30Avg)) score += 12;
  return Math.min(100, score);
}

function readinessState(data) {
  const sleep = sleepScore(data);
  const move = movementScore(data);
  const recovery = recoveryScore(data);
  if (sleep < 35) return { color: 'yellow', text: '黄色：数据采集修复期', action: '先把睡眠采集和运动底盘稳定下来' };
  if (recovery >= 75 && move >= 65) return { color: 'green', text: '绿色：可以推进', action: '维持 Zone2，并加入轻力量' };
  return { color: 'yellow', text: '黄色：稳定推进', action: 'Zone2 + 睡眠锚点，不做高强度硬冲' };
}

function weeklyZone2(data) {
  const exercise = data.appleHealth?.metrics?.exerciseMinutes || {};
  const last7Avg = n(exercise.last7Avg);
  const captured = Math.round(last7Avg * 7);
  const target = n(data.nextProtocol?.zone2?.weeklyTargetMinutes, 120);
  return { captured, target, progress: pct(captured, target) };
}

function experimentPlan() {
  return [
    { name: '步数地板', target: '连续 14 天 ≥ 6,500 步', why: '先把能量吞吐底盘拉起来。', progress: 0 },
    { name: 'Zone2 三锚点', target: '周二 / 周四 / 周六', why: '让心肺底盘从偶发变成节律。', progress: 0 },
    { name: '睡眠采集', target: '每周 ≥ 5 晚可用数据', why: '没有睡眠数据，就不能判断恢复。', progress: 0 },
    { name: '饭后 20 分钟', target: '晚饭后轻走', why: '血糖、TG、脂肪肝共同上游动作。', progress: 0 }
  ];
}

function buildSummary(data) {
  const steps = data.appleHealth?.metrics?.steps || {};
  const rhr = data.appleHealth?.metrics?.restingHeartRate || {};
  const hrv = data.appleHealth?.metrics?.hrvMs || {};
  const sleep = data.appleHealth?.metrics?.sleepDurationHours || {};
  const z = weeklyZone2(data);
  const state = readinessState(data);
  return {
    state,
    movementScore: movementScore(data),
    zone2Score: zone2Score(data),
    sleepScore: sleepScore(data),
    recoveryScore: recoveryScore(data),
    weeklyZone2: z,
    facts: {
      avgSteps: n(steps.avg),
      last7Steps: n(steps.last7Avg),
      days8000: n(data.appleHealth?.thresholdCounts?.daysStepsGte8000),
      daysLow: n(data.appleHealth?.thresholdCounts?.daysStepsLt3000),
      rhrFirst: n(rhr.first30Avg),
      rhrLast: n(rhr.last30Avg),
      hrvFirst: n(hrv.first30Avg),
      hrvLast: n(hrv.last30Avg),
      sleepDays: n(sleep.days)
    }
  };
}

async function loadYuanliHealthData() {
  const res = await fetch('data/demo-health.json', { cache: 'no-store' });
  if (!res.ok) throw new Error('data fetch failed');
  const data = await res.json();
  return Object.assign({}, YUANLI_DEFAULT_DATA, data);
}

function mountYuanliDashboard(data) {
  const s = buildSummary(data);
  const q = data.appleHealth?.dataQuality || {};
  const set = (id, html) => { const el = document.getElementById(id); if (el) el.innerHTML = html; };
  const text = (id, value) => { const el = document.getElementById(id); if (el) el.textContent = value; };

  text('dataRange', `${data.appleHealth?.range?.start || '—'} → ${data.appleHealth?.range?.end || '—'} · ${data.appleHealth?.range?.days || 0} 天`);
  text('todayState', s.state.text);
  text('todayAction', s.state.action);
  text('avgSteps', fmt(s.facts.avgSteps));
  text('last7Steps', fmt(s.facts.last7Steps));
  text('zone2Done', `${s.weeklyZone2.captured} / ${s.weeklyZone2.target} min`);
  text('sleepDays', `${s.facts.sleepDays} 天`);
  text('rhrTrend', `${fmt(s.facts.rhrFirst, 1)} → ${fmt(s.facts.rhrLast, 1)} bpm`);
  text('hrvTrend', `${fmt(s.facts.hrvFirst, 1)} → ${fmt(s.facts.hrvLast, 1)} ms`);

  set('rings', [
    ['运动底盘', s.movementScore], ['Zone2', s.zone2Score], ['睡眠采集', s.sleepScore], ['恢复趋势', s.recoveryScore]
  ].map(([name, val]) => `<div class="ring" style="--p:${val}"><b>${val}</b><span>${name}</span></div>`).join(''));

  set('qualityGate', Object.entries({ movement: q.movement, recovery: q.recovery, sleep: q.sleep, bodyComposition: q.bodyComposition }).map(([k, v]) => {
    const l = qualityLabel(v);
    const name = { movement: '运动数据', recovery: '恢复数据', sleep: '睡眠数据', bodyComposition: '体成分' }[k];
    return `<div class="signal"><div><b>${name}</b><small>${v || '待接入'}</small></div><span class="badge ${l.cls}">${l.text}</span></div>`;
  }).join(''));

  const sleepWarning = s.facts.sleepDays < 5;
  set('sleepWarning', sleepWarning ? `<b>睡眠采集未完成</b><p>当前只有 ${s.facts.sleepDays} 天可用睡眠数据。先连续 14 天戴表睡觉，并开启睡眠专注；没有稳定采集前，Agent 不做深度睡眠结论。</p>` : `<b>睡眠采集可用</b><p>睡眠数据已达到基础判断门槛，可以开始追踪入睡窗口和起床窗口。</p>`);

  set('zone2Progress', `<div class="bar"><i style="width:${s.weeklyZone2.progress}%"></i></div><p>本周已捕捉 ${s.weeklyZone2.captured} 分钟，目标 ${s.weeklyZone2.target} 分钟。下一步：周二 35–40 分钟、周四 35–40 分钟、周六 45–60 分钟。</p>`);

  set('experiments', experimentPlan().map((e, idx) => `<div class="experiment"><b>${idx + 1}. ${e.name}</b><span>${e.target}</span><p>${e.why}</p><button data-exp="${e.name}">标记今天完成</button></div>`).join(''));
  document.querySelectorAll('[data-exp]').forEach(btn => btn.addEventListener('click', () => { btn.textContent = '今天已完成'; btn.classList.add('done'); }));
}

window.YuanliHealthAgent = { loadYuanliHealthData, mountYuanliDashboard, buildSummary, movementScore, zone2Score, sleepScore, recoveryScore, weeklyZone2 };
