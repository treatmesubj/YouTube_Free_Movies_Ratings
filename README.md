# YouTube_Free_Movies_Ratings

YouTube currently has over [300 legitimately free movies](https://www.youtube.com/feed/storefront) however, most of them are terrible and YouTube provides no good means of browsing them.
So, I wrote a script to fetch the records of the currently available movies - which are buried deep in ungodly JavaScript in YouTube's pre-rendered HTML - then,
fetch the RottenTomatoes critic & audience scores for each.

Added a function for [Pluto TV](https://pluto.tv/on-demand) as well, but Pluto has a pretty good UI, so I'm not using it in `__main__`. When its combined with YouTube's, it's > 1000 "unique" items, so it's not very useful for any comprehension.

A list of the movies sorted by descending critic score is printed - hopefully, it will save some browsing time.

![alt text](https://github.com/treatmesubj/YouTube_Free_Movies_Ratings/blob/main/Screenshot_20201209-090217_Termux.jpg)
