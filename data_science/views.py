from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import newsaggregator.news_finder_with_cache as nf

news_finder = nf.NewsFinder()


# Create your views here.
def index(request):
    keywords = request.POST.get("keywords")
    is_list = False
    if keywords:
        print(keywords)
        # make keywords to a list
        list_keys = keywords.split()
        # list_news = [('Spain faces a constitutional crisis over Catalonia', '<p><div class="ec-content-image ec-thumbnail content-image-full"><a href="http://cdn.static-economist.com/sites/default/files/images/print-edition/20171021_EUP002_0.jpg" class="ec-enlarge"></a><img src="http://cdn.static-economist.com/sites/default/files/images/print-edition/20171021_EUP002_0.jpg" alt="" title="" width="1280" height="720" width="1280" style="height: auto" /></div></p><p>WITH its mastery of social media and identity politics, the Catalan independence movement is very 21st-century. But the latest chapter in its struggle with the Spanish government has featured an old-fashioned tool: an exchange of letters, delivered by fax. In these Carles Puigdemont, the head of the Generalitat, Catalonia’s government, twice this week refused to clarify or revoke the ambiguous proclamation of independence that he had issued and immediately “suspended” in a speech to his parliament on October 10th. In response, the Spanish government said it will go ahead and seek extraordinary powers to impose constitutional rule in Catalonia.</p><p>Spain is thus entering its worst constitutional crisis since the 1930s. It is the culmination of years of rising discontent in Catalonia, one of the country’s richest regions, which has 7.5m people and its own language and culture. Although Catalonia enjoys broad self-government, many Catalans want it to have more money, more powers, and to...<a href="http://www.economist.com/news/europe/21730450-prime-minister-mariano-rajoy-may-have-set-up-parallel-government-stop-secession-spain?fsrc=rss">Continue reading</a>', 'http://www.economist.com/news/europe/21730450-prime-minister-mariano-rajoy-may-have-set-up-parallel-government-stop-secession-spain?fsrc=rss', "26-10-2017", ['struggle', 'government', 'head', 'continue', 'with', 'carles', 'language', 'movement', 'mastery', 'catalonia', 'proclamation', 'independence', 'rule', 'identity', 'crisis', 'october', 'discontent', 'response', 'tool', 'fax', 'puigdemont', 'culmination', 'power', 'year', 'exchange', 'politics', 'catalonia.spain', 'generalitat', 'medium', 'letter', 'chapter', 'catalan', 'culture', 'country', 'region', 'catalans', 'week', 'parliament', 'speech', 'money', 'people', 'spain'], -6269904007202247645, 0),
        #              ('Catalonia slams Spain for direct rule plans', 'Catalan leaders have insisted they will reject any attempt by Madrid to impose direct rule on their autonomous region, as a political crisis escalates over Catalonia\'s threats to declare independence from Spain.<img src="http://feeds.feedburner.com/~r/rss/edition_europe/~4/S-12xyirQM4" height="1" width="1" alt=""/>', 'http://rss.cnn.com/~r/rss/edition_europe/~3/S-12xyirQM4/index.html', "26-10-2017", ['catalan', 'plan', 'independence', 'slam', 'madrid', 'rule', 'threat', 'region', 'crisis', 'attempt', 'leader', 'spain', 'catalonia'], -451751121610643146, 1),
        #              ('The Catalonia Crisis Has Not Divided Spain, Just Its Media', 'The Catalan journalist Mònica Terribas, center, in the studios of Catalunya Radio in Barcelona. A group of right-wing protesters accused Ms. Terribas of leading Catalans toward independence the way a Rwandan radio station persuaded Hutus to kill Tutsis before the 1994 genocide.', 'https://www.nytimes.com/2017/10/25/world/europe/the-catalonia-crisis-has-not-divided-spain-just-its-media.html?partner=rss&emc=rss', "26-10-2017", ['terribas', 'studio', 'protester', 'hutus', 'group', 'rwandan', 'catalonia', 'station', 'barcelona', 'genocide', 'independence', 'media', 'catalunya', 'a', 'radio', 'journalist', 'monica', 'ms.', 'just', 'center', 'has', 'tutsis', 'catalan', 'crisis', 'catalans', 'radio', 'divided', 'spain', 'way'], 1445747406082408638, 2)]

        list_news = news_finder.get_news_from_keywords(list_keys)
        if len(list_news) > 30:
            list_news = list_news[:30]

        is_list = True
        # labels = news_finder.get_news_categorical_labels(list_news)
        # labeled_news = []
        #
        # for news, label in zip(list_news, labels):
        #     labeled_news.append(news + (label,))
        #
        # list_news = sorted(labeled_news, key=lambda x: x[6])
    else:
        list_news = news_finder.get_all_news_entries()

    context = {'list_news': list_news, 'is_list': is_list}
    return render(request, 'index.html', context)


def related_news(request, entry_id):
    list_related_news = []
    all_news = news_finder.get_all_news_entries()
    news_entry = all_news[int(entry_id)]
    # labels = []
    news_entry = news_entry[:5] + (int(entry_id),)
    print(news_entry)
    if news_entry:
        # news_entry = news_entry[:6]
        list_related_news = news_finder.get_related_news(news_entry, top_entries=10)
        print(list_related_news)
        labels = news_finder.get_news_categorical_labels(list_related_news)
        labeled_news = []

        for news, label in zip(list_related_news, labels):
            labeled_news.append(news + (label,))

        list_related_news = sorted(labeled_news, key=lambda x: x[6])

    context = {'list_related_news': list_related_news}
    return render(request, 'related_news.html', context)

