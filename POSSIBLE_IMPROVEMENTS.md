Development is always a trade-off between features and time/cost. I made some trade-offs in writing this, here are some things that could be improved: 

- Fix floating point issue with adding two float numbers -- sometimes 7.1 + 1.1 gives
8.2000001 for some reason. Python documentation says solution is to use Decimal module,
however this is not immediately serializable for JSON output so we'd have to figure out how to serialize this. 

- Possibly better sorting algorithm for allocating books into boxes. This is related to NP-complete problem called Knapsack problem, so I didn't spend too much time on the perfect solution since input was small and algoritm I used performed well but this could possibly be improved. 

- Make directories and names of files used have full paths and not be hardcoded. 

- Better error handling in the scraping of data. For small amounts of data, the results
are usually quite consistent but over larger data sets, it would better to have more error handling and checking for values that don't appear. 

- Make the JSON output appear in a certain order, with the shorter items appearing first

- "Packed" field doesn't need to appear in the JSON output for a book, would be good to find a way to remove it from the output