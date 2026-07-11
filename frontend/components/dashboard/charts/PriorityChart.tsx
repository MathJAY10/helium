"use client";

import { RankedOpportunity } from "@/types/audit";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

interface PriorityChartProps {
  opportunities: RankedOpportunity[];
}

export function PriorityChart({ opportunities }: PriorityChartProps) {
  const high = opportunities.filter((o) => o.priority_score >= 80).length;
  const medium = opportunities.filter((o) => o.priority_score >= 50 && o.priority_score < 80).length;
  const low = opportunities.filter((o) => o.priority_score < 50).length;

  const data = [
    { name: "High Priority", value: high, color: "#ef4444" },
    { name: "Medium Priority", value: medium, color: "#f59e0b" },
    { name: "Low Priority", value: low, color: "#3b82f6" },
  ].filter((d) => d.value > 0);

  if (data.length === 0) return null;

  return (
    <Card className="col-span-1 h-[300px] flex flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          Priority Distribution
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 pb-4">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ borderRadius: "8px", border: "1px solid #e4e4e7" }}
              itemStyle={{ color: "#18181b", fontSize: "14px", fontWeight: 500 }}
            />
            <Legend verticalAlign="bottom" height={36} iconType="circle" />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
