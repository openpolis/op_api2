from django.core.exceptions import ObjectDoesNotExist
import operator
from parlamento.models import *

# data deve essere una di quelle contenute in OppActHistoryCache
data = '2011-09-12'
tags = ("automobili", "autostrade", "codice della strada", "diritto della circolazione stradale",
        "educazione stradale", "guida in stato di ubriachezza", "patente di guida",
        "sicurezza stradale", "trasporti stradali", "veicoli elettrici",
        'biciclette', 'trasporti', "mobilita' sostenibile", "traffico urbano")

tags_ids = [int(t.id) for t in SfTag.objects.using('parlamento').filter(
    triple_value__in=tags)
]

acts_ids =  [t.get('taggable_id') for t in SfTagging.objects.using('parlamento').filter(
    taggable_model='OppAtto', tag__in=tags_ids
).values('taggable_id').distinct()]

politici = {}
for act_id in acts_ids:
    print "{0}".format(act_id)
    try:
        act_cache = OppActHistoryCache.objects.using('parlamento').get(chi_tipo='A', chi_id=act_id, data=data)
    except ObjectDoesNotExist:
        continue
    firme = OppCaricaHasAtto.objects.using('parlamento').filter(delete_at__isnull=True, data__lte=data, carica__tipo_carica__in=(1,), atto=act_id).values('tipo', 'carica_id')
    for f in firme:
        carica_id = int(f['carica_id'])
        if carica_id not in politici:
            politici[carica_id] = 0
        politici[carica_id] += OppCaricaHasAtto.FATTORE_FIRMA[f['tipo'].upper()] * act_cache.indice / act_cache.priorita

    interventi = act.oppintervento_set.filter(data__lte=data, carica__tipo_carica__in=(1,)).values('carica_id')
    for i in interventi:
        carica_id = int(i['carica_id'])
        if carica_id not in politici:
            politici[carica_id] = 0
        politici[carica_id] += OppCaricaHasAtto.FATTORE_FIRMA['I'] * act_cache.indice / act_cache.priorita


sorted_politici = sorted(politici.iteritems(), key=operator.itemgetter(1), reverse=True)
for p in sorted_politici[0:10]:
    charge = OppCarica.objects.using('parlamento').get(pk=p[0])
    print "{0} => {1}".format(charge.politico, p[1])
