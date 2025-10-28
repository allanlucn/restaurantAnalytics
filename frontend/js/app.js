import { loadMetrics } from './metrics.js';
import { loadChannelChart, loadTimelineChart } from './charts.js';

document.addEventListener('DOMContentLoaded', () => {
    loadMetrics();
    loadChannelChart();
    loadTimelineChart();
});
