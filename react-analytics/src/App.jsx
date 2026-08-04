import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Users, UserCheck, Clock, CreditCard, MapPin, Award, 
  Activity, Bell, Server, Zap, Calendar, TrendingUp, Sparkles, ChevronRight 
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend 
} from 'recharts';

// --- MOCK DATA ENGINE ---
const generateMockData = () => {
  // KPIs
  const kpis = {
    total: { value: 12450, change: '+14.5%', isPositive: true },
    pending: { value: 342, change: '-5.2%', isPositive: true },
    approved: { value: 11850, change: '+16.1%', isPositive: true },
    revenue: { value: '₹14.2M', change: '+22.4%', isPositive: true },
    centres: { value: 45, change: '0%', isPositive: true },
    scholarships: { value: 850, change: '+8.3%', isPositive: true },
  };

  // Trend Data (30 days)
  const trendData = Array.from({ length: 30 }).map((_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (29 - i));
    return {
      date: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      registrations: Math.floor(Math.random() * 500) + 200 + (i * 10)
    };
  });

  // Exam Distribution
  const distributionData = [
    { name: 'SET Session 1', value: 4500, color: '#8b5cf6' },
    { name: 'SET Session 2', value: 3800, color: '#3b82f6' },
    { name: 'Scholarship Test', value: 2150, color: '#ec4899' },
    { name: 'Admission Test', value: 2000, color: '#10b981' }
  ];

  // Application Funnel
  const funnelData = [
    { label: 'Registered', value: 12450 },
    { label: 'Paid', value: 11800 },
    { label: 'Verified', value: 11450 },
    { label: 'Hall Ticket Generated', value: 11000 },
    { label: 'Appeared', value: 10500 },
    { label: 'Qualified', value: 8400 }
  ];

  // Activity Timeline
  const activityTimeline = [
    { time: '10 mins ago', text: 'System auto-allocated 450 candidates to Bengaluru (HQ).' },
    { time: '1 hour ago', text: 'Payment gateway sync completed successfully.' },
    { time: '3 hours ago', text: 'New admission test dates announced by Controller of Exam.' },
    { time: '5 hours ago', text: '24 scholarship applications approved.' }
  ];

  // Top Cities
  const topCities = [
    { city: 'Bengaluru', percentage: 45 },
    { city: 'Mysuru', percentage: 22 },
    { city: 'Hubballi', percentage: 15 },
    { city: 'Mangaluru', percentage: 10 },
    { city: 'Belagavi', percentage: 8 }
  ];

  return { kpis, trendData, distributionData, funnelData, activityTimeline, topCities };
};


// --- UI COMPONENTS ---
const Card = ({ children, className = '' }) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    whileHover={{ y: -4, boxShadow: '0 20px 40px -10px rgba(0,0,0,0.3)' }}
    className={`bg-slate-800/40 backdrop-blur-md border border-slate-700/50 rounded-2xl p-6 shadow-xl ${className}`}
  >
    {children}
  </motion.div>
);

const KPICard = ({ title, value, change, isPositive, icon: Icon, colorClass }) => (
  <Card className="flex flex-col gap-4">
    <div className="flex justify-between items-start">
      <div>
        <h4 className="text-slate-400 text-sm font-medium uppercase tracking-wider">{title}</h4>
        <div className="text-3xl font-bold text-white mt-1">{value}</div>
      </div>
      <div className={`p-3 rounded-xl ${colorClass}`}>
        <Icon size={24} className="text-white" />
      </div>
    </div>
    <div className="flex items-center gap-2">
      <span className={`text-sm font-bold ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
        {change}
      </span>
      <span className="text-slate-500 text-sm">vs last month</span>
    </div>
  </Card>
);

const SectionTitle = ({ title, subtitle, icon: Icon }) => (
  <div className="mb-6">
    <div className="flex items-center gap-2 mb-1">
      {Icon && <Icon size={20} className="text-brand-primary" />}
      <h3 className="text-xl font-bold text-white">{title}</h3>
    </div>
    {subtitle && <p className="text-slate-400 text-sm">{subtitle}</p>}
  </div>
);


// --- MAIN APP ---
export default function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // In a real integration, we could check window.firebaseData here.
    // For this implementation, we use the realistic mock generator.
    setData(generateMockData());
  }, []);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-screen w-full">
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="w-12 h-12 rounded-full border-4 border-brand-primary border-t-transparent animate-spin"></div>
          <p className="text-slate-400 font-medium tracking-wide">Loading Enterprise Analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-[1600px] mx-auto space-y-6 pb-20">
      
      {/* KPIs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
        <KPICard title="Total Reg" value={data.kpis.total.value.toLocaleString()} change={data.kpis.total.change} isPositive={data.kpis.total.isPositive} icon={Users} colorClass="bg-brand-primary/80" />
        <KPICard title="Pending" value={data.kpis.pending.value} change={data.kpis.pending.change} isPositive={data.kpis.pending.isPositive} icon={Clock} colorClass="bg-amber-500/80" />
        <KPICard title="Approved" value={data.kpis.approved.value.toLocaleString()} change={data.kpis.approved.change} isPositive={data.kpis.approved.isPositive} icon={UserCheck} colorClass="bg-emerald-500/80" />
        <KPICard title="Revenue" value={data.kpis.revenue.value} change={data.kpis.revenue.change} isPositive={data.kpis.revenue.isPositive} icon={CreditCard} colorClass="bg-brand-secondary/80" />
        <KPICard title="Centres" value={data.kpis.centres.value} change={data.kpis.centres.change} isPositive={data.kpis.centres.isPositive} icon={MapPin} colorClass="bg-brand-tertiary/80" />
        <KPICard title="Scholarships" value={data.kpis.scholarships.value} change={data.kpis.scholarships.change} isPositive={data.kpis.scholarships.isPositive} icon={Award} colorClass="bg-rose-500/80" />
      </div>

      {/* Main Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Registration Trend */}
        <Card className="lg:col-span-2">
          <SectionTitle title="Registration Trend" subtitle="30-day overview of candidate applications" icon={TrendingUp} />
          <div className="h-[350px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.trendData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorReg" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="date" stroke="#64748b" tick={{ fill: '#64748b', fontSize: 12 }} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" tick={{ fill: '#64748b', fontSize: 12 }} tickLine={false} axisLine={false} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="registrations" stroke="#8b5cf6" strokeWidth={3} fillOpacity={1} fill="url(#colorReg)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Exam Distribution */}
        <Card>
          <SectionTitle title="Exam Distribution" subtitle="Active candidates across exam types" icon={PieChart} />
          <div className="h-[350px] w-full flex flex-col justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.distributionData}
                  cx="50%"
                  cy="45%"
                  innerRadius={80}
                  outerRadius={110}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {data.distributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#fff' }}
                />
                <Legend verticalAlign="bottom" height={36} iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Application Funnel */}
      <Card>
        <SectionTitle title="Application Funnel" subtitle="Candidate progression through the examination lifecycle" icon={Activity} />
        <div className="flex flex-col md:flex-row justify-between items-center w-full mt-8 mb-4 gap-4 md:gap-0">
          {data.funnelData.map((step, index) => (
            <React.Fragment key={index}>
              <div className="flex flex-col items-center text-center relative w-full md:w-auto">
                <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-brand-primary/40 flex items-center justify-center shadow-[0_0_20px_rgba(139,92,246,0.15)] mb-4">
                  <span className="text-xl font-bold text-white">{((step.value / data.funnelData[0].value) * 100).toFixed(0)}%</span>
                </div>
                <h4 className="text-white font-bold text-lg">{step.value.toLocaleString()}</h4>
                <p className="text-slate-400 text-xs uppercase tracking-wider mt-1">{step.label}</p>
              </div>
              {index < data.funnelData.length - 1 && (
                <div className="hidden md:flex flex-1 h-[2px] bg-slate-700/50 mx-4 relative overflow-hidden">
                  <motion.div 
                    className="absolute top-0 left-0 h-full bg-brand-primary" 
                    initial={{ width: 0 }}
                    animate={{ width: '100%' }}
                    transition={{ duration: 1.5, delay: index * 0.2 }}
                  />
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </Card>

      {/* Lower Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* AI Insights & Notifications */}
        <div className="space-y-6">
          <Card>
            <SectionTitle title="AI Insights" subtitle="Automated intelligence recommendations" icon={Sparkles} />
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex gap-3">
                <div className="text-indigo-400 mt-1"><Sparkles size={18} /></div>
                <div>
                  <h5 className="text-white text-sm font-bold mb-1">Capacity Warning</h5>
                  <p className="text-slate-400 text-xs leading-relaxed">Bengaluru (HQ) centre is nearing 90% capacity. Consider allocating overflow to Mysuru.</p>
                </div>
              </div>
              <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex gap-3">
                <div className="text-emerald-400 mt-1"><TrendingUp size={18} /></div>
                <div>
                  <h5 className="text-white text-sm font-bold mb-1">Registration Spike</h5>
                  <p className="text-slate-400 text-xs leading-relaxed">Scholarship applications up 24% this week. Ensure document verification team is scaled.</p>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between mb-4">
              <SectionTitle title="System Status" />
              <div className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span className="text-emerald-400 text-xs font-bold uppercase tracking-wider">All Systems Operational</span>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 bg-slate-800/50 rounded-lg">
                <div className="text-slate-400 text-xs mb-1">Server Load</div>
                <div className="text-white font-mono">24.5%</div>
              </div>
              <div className="p-3 bg-slate-800/50 rounded-lg">
                <div className="text-slate-400 text-xs mb-1">Database Sync</div>
                <div className="text-white font-mono">Synced</div>
              </div>
              <div className="p-3 bg-slate-800/50 rounded-lg">
                <div className="text-slate-400 text-xs mb-1">API Latency</div>
                <div className="text-white font-mono">42ms</div>
              </div>
              <div className="p-3 bg-slate-800/50 rounded-lg">
                <div className="text-slate-400 text-xs mb-1">Active Sessions</div>
                <div className="text-white font-mono">1,245</div>
              </div>
            </div>
          </Card>
        </div>

        {/* Timeline & Events */}
        <Card className="lg:col-span-2">
          <SectionTitle title="Command Center" subtitle="Recent activity and geographical metrics" icon={Server} />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Timeline */}
            <div>
              <h4 className="text-white text-sm font-bold mb-6 flex items-center gap-2"><Bell size={16} className="text-slate-400"/> Activity Timeline</h4>
              <div className="space-y-6 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
                {data.activityTimeline.map((item, i) => (
                  <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div className="flex items-center justify-center w-5 h-5 rounded-full border-2 border-slate-700 bg-slate-900 text-brand-primary shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10"></div>
                    <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-xl border border-slate-700/50 bg-slate-800/30">
                      <div className="flex items-center justify-between mb-1">
                        <time className="text-xs font-medium text-brand-primary">{item.time}</time>
                      </div>
                      <div className="text-slate-300 text-sm leading-relaxed">{item.text}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Cities Progress Bars */}
            <div>
              <h4 className="text-white text-sm font-bold mb-6 flex items-center gap-2"><MapPin size={16} className="text-slate-400"/> Top Performing Cities</h4>
              <div className="space-y-5">
                {data.topCities.map((city, i) => (
                  <div key={i}>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-slate-300 font-medium">{city.city}</span>
                      <span className="text-white font-bold">{city.percentage}%</span>
                    </div>
                    <div className="w-full bg-slate-700/50 rounded-full h-2">
                      <motion.div 
                        className="bg-gradient-to-r from-brand-secondary to-brand-primary h-2 rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${city.percentage}%` }}
                        transition={{ duration: 1, delay: 0.5 + (i * 0.1) }}
                      ></motion.div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-8 p-4 rounded-xl border border-slate-700/50 bg-slate-800/30">
                <h4 className="text-white text-sm font-bold mb-3 flex items-center gap-2"><Calendar size={16} className="text-slate-400"/> Upcoming Events</h4>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between border-b border-slate-700/50 pb-2">
                    <span className="text-slate-400">SET Admit Card Release</span>
                    <span className="text-emerald-400 font-medium">Tomorrow, 10:00 AM</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Scholarship Exam</span>
                    <span className="text-white font-medium">Aug 15, 2026</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>

      </div>
    </div>
  );
}
