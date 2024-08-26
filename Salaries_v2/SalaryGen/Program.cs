using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using Wkffl.SalaryGen.Parsers;
using Wkffl.SalaryGen.Players;

namespace Wkffl.SalaryGen
{
    internal class Program
    {
        private static readonly Random _seed = new Random();

        static void Main(string[] args)
        {
            string year = "2024";
            if (args.Length == 1)
            {
                year = args[0];
            }

            Dictionary<string, RankingPlayer> aggregatePlayers = new Dictionary<string, RankingPlayer>();

            foreach (RankingsType type in Enum.GetValues<RankingsType>())
            {
                StreamReader streamReader = File.OpenText($"E:\\joshw\\source\\repos\\wkffl\\Salaries_v2\\SalaryGen\\Adp\\{year}\\{type}.csv");

                // Skip the header
                streamReader.ReadLine();

                FantasyProsAdpParser parser = new FantasyProsAdpParser();
                using (streamReader)
                {
                    while (!streamReader.EndOfStream)
                    {
                        string lineVal = streamReader.ReadLine();
                        if (lineVal == @"""" || string.IsNullOrWhiteSpace(lineVal))
                        {
                            continue;
                        }

                        string[] splitLine = lineVal.Split(',');
                        if (splitLine.Length <= 1)
                        {
                            continue;
                        }

                        ParsedPlayer player = parser.ParsePlayerLine(splitLine);

                        if (!aggregatePlayers.ContainsKey(player.Player.Identifier))
                        {
                            aggregatePlayers.Add(player.Player.Identifier, player.Player);
                        }

                        aggregatePlayers[player.Player.Identifier].AddRanking(type, player.OverallRanking, player.PositionRanking, player.AvgRanking);
                    }
                }
            }

            IEnumerable<IGrouping<string, RankingPlayer>> playersByPosition = aggregatePlayers.Values.GroupBy(p => p.Position);
            foreach (IGrouping<string, RankingPlayer> posGroup in playersByPosition)
            {
                List<SalaryPlayer> rankedPlayers = new List<SalaryPlayer>();

                foreach (RankingPlayer player in posGroup.OrderBy(p => p.PositionRanking).Take(_salaries[posGroup.Key].Count()))
                {
                    double fudgeFactor = _seed.NextDouble() * (1.10 - 0.9) + 0.9;

                    double salary = CalculateRollingAvg(player.Position, player.PositionRanking * fudgeFactor);
                    Console.WriteLine($"{player.Position},{player.Name},{Math.Round(salary, 1)},{player.Team}");

                    rankedPlayers.Add(new SalaryPlayer(player, salary));
                }

                using (StreamWriter fileWriter = new StreamWriter($".\\{year}\\{posGroup.Key}.csv"))
                { 
                    foreach (SalaryPlayer player in rankedPlayers.OrderByDescending(p => p.Salary))
                    {
                        fileWriter.WriteLine($"{player.Player.Name},{Math.Round(player.Salary, 1)},{player.Player.Team}");
                    }
                }
            }
        }

        private static readonly IReadOnlyDictionary<string, double[]> _salaries = new Dictionary<string, double[]>
        { 
            ["QB"] = new double[] { 20.0, 19.3, 18.8, 18.3, 17.9, 17.5, 17.3, 17.0, 16.9, 16.8, 16.6, 16.3, 16.1, 15.9, 15.7, 15.6, 15.5, 15.3, 15.3, 15.2, 15.1, 15.1, 15.0, 15.0, 15.0, 15.0, 14.9, 14.8, 14.7, 14.7, 14.6, 14.6, 14.5, 14.5, 14.5, 14.5, 14.4, 14.4, 14.4, 14.3, 14.3, 14.3, 14.2, 14.2, 14.1, 14.1, 14.0, 14.0, 14.0, 14.0, 13.9, 13.9, 13.8, 13.8, 13.7, 13.6, 13.6, 13.5, 13.5, 13.4, 13.4, 13.4, 13.3, 13.2, 13.2, 13.2, 13.2, 13.2, 13.1, 13.1, 13.1, 13.1, 13.0, 13.0, 13.0, 13.0 },
            ["RB"] = new double[] { 16.0, 15.7, 15.1, 14.7, 14.3, 14.0, 13.9, 13.6, 13.3, 12.8, 12.6, 12.2, 11.9, 11.6, 11.2, 11.1, 11.0, 10.9, 10.7, 10.5, 10.4, 10.2, 10.0, 9.9, 9.8, 9.7, 9.6, 9.5, 9.5, 9.4, 9.3, 9.1, 9.0, 9.0, 8.9, 8.9, 8.8, 8.7, 8.6, 8.5, 8.4, 8.3, 8.3, 8.2, 8.1, 8.1, 8.0, 7.9, 7.9, 7.8, 7.7, 7.6, 7.5, 7.4, 7.4, 7.3, 7.2, 7.1, 7.0, 7.0, 6.9, 6.9, 6.8, 6.7, 6.6, 6.5, 6.4, 6.3, 6.2, 6.1, 6.1, 6.0, 6.0, 5.9, 5.9, 5.8, 5.7, 5.6, 5.6, 5.5, 5.4, 5.3, 5.2, 5.1, 5.1, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.9, 4.9, 4.9, 4.9, 4.8, 4.8, 4.8, 4.8, 4.7, 4.7, 4.7, 4.7, 4.6, 4.6, 4.6, 4.5, 4.5, 4.5, 4.4, 4.4, 4.3, 4.2, 4.2, 4.1, 4.1, 4.0, 4.0, 4.0, 3.9, 3.9, 3.8, 3.8, 3.7, 3.7, 3.7, 3.6, 3.6, 3.6, 3.6, 3.5, 3.5, 3.5 },
            ["WR"] = new double[] { 13.5, 13.3, 13.0, 12.8, 12.5, 12.4, 12.3, 11.8, 11.3, 10.8, 10.4, 10.2, 10.0, 9.9, 9.8, 9.7, 9.6, 9.5, 9.5, 9.4, 9.3, 9.3, 9.2, 9.1, 9.0, 9.0, 9.0, 8.9, 8.8, 8.7, 8.7, 8.7, 8.6, 8.6, 8.5, 8.5, 8.4, 8.4, 8.3, 8.3, 8.2, 8.2, 8.1, 8.1, 8.0, 8.0, 8.0, 7.9, 7.9, 7.8, 7.8, 7.7, 7.7, 7.6, 7.5, 7.5, 7.5, 7.4, 7.3, 7.3, 7.2, 7.2, 7.1, 7.0, 7.0, 6.9, 6.9, 6.8, 6.8, 6.7, 6.6, 6.6, 6.5, 6.5, 6.4, 6.4, 6.3, 6.3, 6.2, 6.1, 6.1, 6.0, 6.0, 6.0, 5.9, 5.9, 5.8, 5.8, 5.7, 5.6, 5.5, 5.5, 5.5, 5.5, 5.4, 5.4, 5.4, 5.3, 5.3, 5.3, 5.3, 5.2, 5.2, 5.2, 5.2, 5.1, 5.1, 5.0, 5.0, 5.0, 4.9, 4.9, 4.8, 4.8, 4.8, 4.8, 4.7, 4.7, 4.7, 4.6, 4.6, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.4, 4.4, 4.4, 4.4, 4.4, 4.3, 4.3, 4.3, 4.3, 4.3, 4.3, 4.2, 4.2, 4.2, 4.2, 4.2, 4.1, 4.1, 4.1, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.7, 3.7, 3.7, 3.7, 3.6, 3.6, 3.6, 3.6, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5 },
            ["TE"] = new double[] { 7.5, 6.9, 6.5, 6.3, 6.3, 6.2, 6.2, 6.0, 5.9, 5.8, 5.7, 5.5, 5.4, 5.3, 5.2, 5.2, 5.1, 5.0, 5.0, 5.0, 4.9, 4.9, 4.8, 4.7, 4.7, 4.6, 4.5, 4.5, 4.4, 4.3, 4.3, 4.2, 4.1, 4.0, 3.9, 3.9, 3.9, 3.9, 3.8, 3.8, 3.7, 3.7, 3.7, 3.7, 3.6, 3.6, 3.5, 3.5, 3.5, 3.5, 3.4, 3.4, 3.4, 3.3, 3.3, 3.3, 3.3, 3.2, 3.2, 3.2, 3.2, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.9, 2.9, 2.9, 2.9, 2.9, 2.9 },
            ["K"] = new double[] { 8.0, 7.8, 7.3, 7.0, 6.9, 6.8, 6.7, 6.6, 6.5, 6.4, 6.4, 6.4, 6.3, 6.3, 6.3, 6.2, 6.2, 6.2, 6.2, 6.1, 6.1, 6.1, 6.1, 6.0, 6.0, 5.9, 5.9, 5.8, 5.8, 5.7, 5.7, 5.7, 5.6, 5.5, 5.5, 5.4, 5.3, 5.2, 5.1, 5.0 },
            ["DST"] = new double[] { 14.5, 14.2, 13.8, 13.5, 13.4, 13.2, 13.1, 13.0, 13.0, 12.9, 12.9, 12.8, 12.8, 12.7, 12.6, 12.6, 12.5, 12.5, 12.4, 12.3, 12.3, 12.2, 12.2, 12.1, 12.0, 12.0, 11.9, 11.8, 11.5, 11.4, 11.2, 11.0 },
        };

        private static double CalculateRollingAvg(string position, double positionRanking)
        {
            double[] salaries = _salaries[position];

            int index = (int)Math.Round(positionRanking);

            double withinRange = positionRanking - index;

            int topRange = index - 2 < 0 ? 0 : index - 2;

            if (topRange >= salaries.Length)
            {
                topRange = salaries.Length - 1;
            }

            int numVals = index < 2 || index > (salaries.Length - 3) ? 1 : 5;

            ArraySegment<double> segment = new ArraySegment<double>(salaries, topRange, numVals);
            double rollingAvg = segment.Average();
            double stdDev = segment.CalculateStandardDeviation();

            return rollingAvg + (stdDev * withinRange);
        }
    }

    internal static class Extensions
    {
        public static double CalculateStandardDeviation(this IEnumerable<double> values)
        {
            double standardDeviation = 0;

            if (values.Any())
            {
                double avg = values.Average();
                return Math.Sqrt(values.Average(v => Math.Pow(v - avg, 2)));
            }

            return standardDeviation;
        }
    }
}