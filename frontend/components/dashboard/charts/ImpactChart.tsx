"use client";

import { RankedOpportunity } from "@/types/audit";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from "recharts";

interface ImpactChartProps {
  opportunities: RankedOpportunity[];
}

export function ImpactChart({ opportunities }: ImpactChartProps) {
  const impacts = {
    HIGH: opportunities.filter((o) => o.impact === "HIGH").length,
    MEDIUM: opportunities.filter((o) => o.impact === "MEDIUM").length,
    LOW: opportunities.filter((o) => o.impact === "LOW").length,
  };

  const data = [
    { name: "High", count: impacts.HIGH, color: "#10b981" }, // emerald
    { name: "Medium", count: impacts.MEDIUM, color: "#f59e0b" }, // amber
    { name: "Low", count: impacts.LOW, color: "#64748b" }, // slate
  ];

  if (data.every(d => d.count === 0)) return null;

  return (
    <Card className="col-span-1 h-[300px] flex flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          Impact Distribution
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 pb-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 20, right: 20, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tickLine={false} axisLine={false} />
            <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
            <Tooltip 
              cursor={{ fill: '#f4f4f5' }}
              contentStyle={{ borderRadius: "8px", border: "1px solid #e4e4e7" }}
            />
            <Bar dataKey="count" radius={[4, 4, 0, 0]} barSize={40}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
