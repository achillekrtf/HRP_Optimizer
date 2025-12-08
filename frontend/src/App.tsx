import { useState, useEffect } from 'react'
import axios from 'axios'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip } from 'recharts'
import { Activity, TrendingUp, ShieldAlert, RefreshCw } from 'lucide-react'

// ... (rest of imports/interfaces same)

// ...

// Inside component
<div className="h-[300px] w-full">
  <ResponsiveContainer width="100%" height="100%">
    <PieChart>
      <Pie
        data={pieData}
        cx="50%"
        cy="50%"
        innerRadius={60}
        outerRadius={100}
        paddingAngle={5}
        dataKey="value"
      >
        {pieData.map((_, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="rgba(0,0,0,0)" />
        ))}
      </Pie>
      <RechartsTooltip
        contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }}
        itemStyle={{ color: '#f8fafc' }}
      />
    </PieChart>
  </ResponsiveContainer>
</div>
// ...

// Types
interface Metrics {
  expected_return: number
  volatility: number
  sharpe_ratio: number
}

interface AllocationData {
  date: string
  weights: Record<string, number>
  metrics: Metrics
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function App() {
  const [allocation, setAllocation] = useState<AllocationData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchData = async () => {
    try {
      setLoading(true)
      const res = await axios.get(`${API_URL}/allocation`)
      setAllocation(res.data)
      setError('')
    } catch (err) {
      console.error(err)
      setError('Failed to fetch data. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleRebalance = async () => {
    try {
      await axios.post(`${API_URL}/rebalance`)
      alert('Rebalance triggered! Refresh in a few moments.')
      fetchData()
    } catch (err) {
      alert('Failed to trigger rebalance.')
    }
  }

  if (loading) return <div className="flex h-screen items-center justify-center text-white">Loading Dashboard...</div>
  if (error) return <div className="flex h-screen items-center justify-center text-red-400">{error}</div>
  if (!allocation) return <div className="flex h-screen items-center justify-center text-white">No Data Available</div>

  // Prepare Chart Data
  const pieData = Object.entries(allocation.weights).map(([name, value]) => ({
    name,
    value: value * 100
  })).filter(d => d.value > 0.01) // Filter tiny holdings

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#6366f1']

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <header className="max-w-7xl mx-auto mb-10 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            Tech Giants HRP Dashboard
          </h1>
          <p className="text-slate-400 mt-2">
            Last Rebalance: <span className="text-slate-200">{allocation.date}</span>
          </p>
        </div>
        <button
          onClick={handleRebalance}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition border border-slate-700 hover:border-blue-500"
        >
          <RefreshCw size={18} /> Rebalance Now
        </button>
      </header>

      <main className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Metrics Cards */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-2 text-blue-400">
            <TrendingUp size={24} />
            <h3 className="font-medium">Expected Return</h3>
          </div>
          <p className="text-3xl font-bold text-white">
            {(allocation.metrics.expected_return * 100).toFixed(2)}%
          </p>
          <span className="text-xs text-slate-500">Annualized</span>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-2 text-amber-400">
            <Activity size={24} />
            <h3 className="font-medium">Volatility</h3>
          </div>
          <p className="text-3xl font-bold text-white">
            {(allocation.metrics.volatility * 100).toFixed(2)}%
          </p>
          <span className="text-xs text-slate-500">Annualized Risk</span>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-2 text-emerald-400">
            <ShieldAlert size={24} />
            <h3 className="font-medium">Sharpe Ratio</h3>
          </div>
          <p className="text-3xl font-bold text-white">
            {allocation.metrics.sharpe_ratio.toFixed(2)}
          </p>
          <span className="text-xs text-slate-500">Risk-Adjusted Return</span>
        </div>

        {/* Charts */}
        <div className="md:col-span-2 bg-slate-800/50 p-6 rounded-xl border border-slate-700 min-h-[400px]">
          <h3 className="text-xl font-semibold mb-6">Asset Allocation</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="rgba(0,0,0,0)" />
                  ))}
                </Pie>
                <RechartsTooltip
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }}
                  itemStyle={{ color: '#f8fafc' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-wrap gap-4 mt-4 justify-center">
            {pieData.map((d, i) => (
              <div key={d.name} className="flex items-center gap-2 text-sm">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                <span>{d.name} ({d.value.toFixed(1)}%)</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
          <h3 className="text-xl font-semibold mb-4">Strategy Info</h3>
          <p className="text-slate-400 text-sm leading-relaxed">
            This portfolio uses <strong>Hierarchical Risk Parity (HRP)</strong> to allocate capital.
            Unlike Mean-Variance Optimization, HRP does not require inverting a covariance matrix,
            making it robust to noise and shocks.
            <br /><br />
            The algorithm clusters assets based on correlation and allocates risk recursively
            to achieve diversification.
          </p>
        </div>
      </main>
    </div>
  )
}

export default App
