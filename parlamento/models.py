# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib.contenttypes import generic

class OppActHistoryCache(models.Model):
    legislatura = models.IntegerField(null=True, blank=True)
    data = models.DateField(unique=True)
    indice = models.FloatField(null=True, blank=True, help_text="Index of relevancy for the act, computed at the given date")
    chi_tipo = models.CharField(max_length=1, unique=True)
    chi_id = models.IntegerField()
    tipo_atto_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    indice_pos = models.IntegerField(null=True, blank=True)
    indice_delta = models.FloatField(null=True, blank=True)
    priorita = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_act_history_cache'
        managed = False

class OppPoliticianHistoryCache(models.Model):
    legislatura = models.IntegerField(null=True, blank=True)
    data = models.DateField(unique=True)
    assenze = models.FloatField(null=True, blank=True)
    presenze = models.FloatField(null=True, blank=True)
    missioni = models.FloatField(null=True, blank=True)
    indice = models.FloatField(null=True, blank=True)
    ribellioni = models.FloatField(null=True, blank=True)
    chi_tipo = models.CharField(max_length=1, unique=True)
    chi_id = models.IntegerField()
    ramo = models.CharField(max_length=1, unique=True)
    numero = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    gruppo_id = models.IntegerField(null=True, blank=True)
    assenze_delta = models.FloatField(null=True, blank=True)
    presenze_delta = models.FloatField(null=True, blank=True)
    missioni_delta = models.FloatField(null=True, blank=True)
    indice_delta = models.FloatField(null=True, blank=True)
    ribellioni_delta = models.FloatField(null=True, blank=True)
    assenze_pos = models.IntegerField(null=True, blank=True)
    presenze_pos = models.IntegerField(null=True, blank=True)
    missioni_pos = models.IntegerField(null=True, blank=True)
    indice_pos = models.IntegerField(null=True, blank=True)
    ribellioni_pos = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_politician_history_cache'
        managed = False

class OppTagHistoryCache(models.Model):
    legislatura = models.IntegerField(null=True, blank=True)
    data = models.DateField(unique=True)
    indice = models.FloatField(null=True, blank=True)
    chi_tipo = models.CharField(max_length=1, unique=True)
    chi_id = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    indice_pos = models.IntegerField(null=True, blank=True)
    indice_delta = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'opp_tag_history_cache'
        managed = False


class OppTipoAtto(models.Model):
    denominazione = models.CharField(max_length=60, blank=True)
    descrizione = models.CharField(max_length=60, blank=True)
    spiegazione = models.TextField(blank=True)
    class Meta:
        db_table = u'opp_tipo_atto'
        managed = False

class OppAtto(models.Model):
    parlamento_id = models.IntegerField(null=True, blank=True)
    tipo_atto = models.ForeignKey(OppTipoAtto)
    ramo = models.CharField(max_length=1, blank=True)
    numfase = models.CharField(max_length=255, blank=True)
    legislatura = models.IntegerField(null=True, blank=True)
    data_pres = models.DateField(null=True, blank=True)
    data_agg = models.DateField(null=True, blank=True)
    titolo = models.TextField(blank=True)
    iniziativa = models.IntegerField(null=True, blank=True)
    completo = models.IntegerField(null=True, blank=True)
    descrizione = models.TextField(blank=True)
    seduta = models.IntegerField(null=True, blank=True)
    pred = models.IntegerField(null=True, blank=True)
    succ = models.IntegerField(null=True, blank=True)
    voto_medio = models.FloatField(null=True, blank=True)
    nb_commenti = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    stato_cod = models.CharField(max_length=2, blank=True)
    stato_fase = models.CharField(max_length=255, blank=True)
    stato_last_date = models.DateTimeField(null=True, blank=True)
    n_monitoring_users = models.IntegerField()
    ut_fav = models.IntegerField()
    ut_contr = models.IntegerField()
    n_interventi = models.IntegerField()
    titolo_aggiuntivo = models.TextField(blank=True)
    is_main_unified = models.IntegerField()
    is_omnibus = models.IntegerField()
    md5 = models.CharField(max_length=255, blank=True)

    firmatari = models.ManyToManyField('OppCarica', through='OppCaricaHasAtto', related_name='atti_firmati')

    class Meta:
        db_table = u'opp_atto'
        managed = False

class OppSede(models.Model):
    codice = models.CharField(max_length=255, blank=True)
    ramo = models.CharField(max_length=255, blank=True)
    denominazione = models.CharField(max_length=255, blank=True)
    legislatura = models.IntegerField(null=True, blank=True)
    tipologia = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_sede'
        managed = False

class OppPolitico(models.Model):
    nome = models.CharField(max_length=30, blank=True)
    cognome = models.CharField(max_length=30, blank=True)
    n_monitoring_users = models.IntegerField()
    sesso = models.CharField(max_length=1, blank=True)

    def __unicode__(self):
        return u"{0} {1}".format(self.nome, self.cognome)

    class Meta:
        db_table = u'opp_politico'
        managed = False


class OppTipoCarica(models.Model):
    nome = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_tipo_carica'
        managed = False


class OppCarica(models.Model):
    politico = models.ForeignKey(OppPolitico)
    tipo_carica = models.ForeignKey(OppTipoCarica)
    carica = models.CharField(max_length=30, blank=True)
    data_inizio = models.DateField(null=True, blank=True)
    data_fine = models.DateField(null=True, blank=True)
    legislatura = models.IntegerField(null=True, blank=True)
    circoscrizione = models.CharField(max_length=60, blank=True)
    presenze = models.IntegerField(null=True, blank=True)
    assenze = models.IntegerField(null=True, blank=True)
    missioni = models.IntegerField(null=True, blank=True)
    parliament_id = models.IntegerField(null=True, blank=True)
    indice = models.FloatField(null=True, blank=True)
    scaglione = models.IntegerField(null=True, blank=True)
    posizione = models.IntegerField(null=True, blank=True)
    media = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    ribelle = models.IntegerField(null=True, blank=True)
    maggioranza_sotto = models.IntegerField()
    maggioranza_sotto_assente = models.IntegerField()
    maggioranza_salva = models.IntegerField()
    maggioranza_salva_assente = models.IntegerField()
    class Meta:
        db_table = u'opp_carica'
        managed = False

class OppCaricaHasAtto(models.Model):

    FATTORE_FIRMA = {
        'P': 1.0,
        'R': 1.0,
        'C': 0.1,
        'I': 0.01,
    }
    atto = models.ForeignKey(OppAtto)
    carica = models.ForeignKey(OppCarica)
    tipo = models.CharField(max_length=255)
    data = models.DateField(null=True, blank=True)
    url = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    delete_at = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'opp_carica_has_atto'
        managed = False

class OppIntervento(models.Model):
    atto = models.ForeignKey(OppAtto)
    carica = models.ForeignKey(OppCarica)
    tipologia = models.CharField(max_length=255, blank=True)
    url = models.TextField(blank=True)
    data = models.DateField(null=True, blank=True)
    sede = models.ForeignKey(OppSede)
    numero = models.IntegerField(null=True, blank=True)
    ap = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    ut_fav = models.IntegerField()
    ut_contr = models.IntegerField()
    class Meta:
        db_table = u'opp_intervento'
        managed = False


class SfTag(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True)
    is_triple = models.IntegerField(null=True, blank=True)
    triple_namespace = models.CharField(max_length=100, blank=True)
    triple_key = models.CharField(max_length=100, blank=True)
    triple_value = models.CharField(max_length=255, blank=True)
    is_tmp = models.IntegerField()
    n_monitoring_users = models.IntegerField()
    class Meta:
        db_table = u'sf_tag'
        managed = False

class SfTagging(models.Model):
    tag = models.ForeignKey(SfTag)
    taggable_model = models.CharField(max_length=30, blank=True)
    taggable_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_tagging'
        managed = False


"""
class DeppApiKeys(models.Model):
    id = models.IntegerField(primary_key=True)
    req_name = models.CharField(max_length=128)
    req_contact = models.CharField(max_length=255)
    req_description = models.TextField(blank=True)
    value = models.CharField(max_length=64)
    requested_at = models.DateTimeField(null=True, blank=True)
    granted_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    refused_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'depp_api_keys'

class NahoWikiContent(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField(blank=True)
    gz_content = models.TextField(blank=True)
    class Meta:
        db_table = u'naho_wiki_content'

class NahoWikiPage(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=True)
    latest_revision = models.IntegerField()
    class Meta:
        db_table = u'naho_wiki_page'

class NahoWikiRevision(models.Model):
    created_at = models.DateTimeField(null=True, blank=True)
    page = models.ForeignKey(NahoWikiPage, primary_key=True)
    revision = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True)
    content = models.ForeignKey(NahoWikiContent)
    class Meta:
        db_table = u'naho_wiki_revision'

class OppActHistoryCache(models.Model):
    id = models.IntegerField(primary_key=True)
    legislatura = models.IntegerField(null=True, blank=True)
    data = models.DateField(unique=True)
    indice = models.FloatField(null=True, blank=True)
    chi_tipo = models.CharField(max_length=1, unique=True)
    chi_id = models.IntegerField()
    tipo_atto_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    indice_pos = models.IntegerField(null=True, blank=True)
    indice_delta = models.FloatField(null=True, blank=True)
    priorita = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_act_history_cache'

class OppAlertTerm(models.Model):
    id = models.IntegerField(primary_key=True)
    term = models.CharField(max_length=128, unique=True)
    n_alerts = models.IntegerField()
    class Meta:
        db_table = u'opp_alert_term'

class OppAlertUser(models.Model):
    user = models.ForeignKey(OppUser)
    term = models.ForeignKey(OppAlertTerm)
    created_at = models.DateTimeField(null=True, blank=True)
    type_filters = models.CharField(max_length=512, blank=True)
    class Meta:
        db_table = u'opp_alert_user'

class OppAppoggio(models.Model):
    id = models.IntegerField(primary_key=True)
    carica = models.ForeignKey(OppCarica)
    aka = models.CharField(max_length=60, blank=True)
    tipologia = models.IntegerField(null=True, blank=True)
    legislatura = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_appoggio'

class OppAtto(models.Model):
    id = models.IntegerField(primary_key=True)
    parlamento_id = models.IntegerField(null=True, blank=True)
    tipo_atto = models.ForeignKey(OppTipoAtto)
    ramo = models.CharField(max_length=1, blank=True)
    numfase = models.CharField(max_length=255, blank=True)
    legislatura = models.IntegerField(null=True, blank=True)
    data_pres = models.DateField(null=True, blank=True)
    data_agg = models.DateField(null=True, blank=True)
    titolo = models.TextField(blank=True)
    iniziativa = models.IntegerField(null=True, blank=True)
    completo = models.IntegerField(null=True, blank=True)
    descrizione = models.TextField(blank=True)
    seduta = models.IntegerField(null=True, blank=True)
    pred = models.IntegerField(null=True, blank=True)
    succ = models.IntegerField(null=True, blank=True)
    voto_medio = models.FloatField(null=True, blank=True)
    nb_commenti = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    stato_cod = models.CharField(max_length=2, blank=True)
    stato_fase = models.CharField(max_length=255, blank=True)
    stato_last_date = models.DateTimeField(null=True, blank=True)
    n_monitoring_users = models.IntegerField()
    ut_fav = models.IntegerField()
    ut_contr = models.IntegerField()
    n_interventi = models.IntegerField()
    titolo_aggiuntivo = models.TextField(blank=True)
    is_main_unified = models.IntegerField()
    is_omnibus = models.IntegerField()
    md5 = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_atto'

class OppAttoHasEmendamento(models.Model):
    emendamento = models.ForeignKey(OppEmendamento)
    atto = models.ForeignKey(OppAtto)
    created_at = models.DateTimeField(null=True, blank=True)
    portante = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_atto_has_emendamento'

class OppAttoHasIter(models.Model):
    id = models.IntegerField(primary_key=True)
    atto = models.ForeignKey(OppAtto)
    iter = models.ForeignKey(OppIter)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_atto_has_iter'

class OppAttoHasSede(models.Model):
    atto = models.ForeignKey(OppAtto)
    sede = models.ForeignKey(OppSede)
    tipo = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_atto_has_sede'

class OppAttoHasTeseo(models.Model):
    atto = models.ForeignKey(OppAtto)
    teseo = models.ForeignKey(OppTeseo)
    class Meta:
        db_table = u'opp_atto_has_teseo'

class OppCarica(models.Model):
    id = models.IntegerField()
    politico = models.ForeignKey(OppPolitico)
    tipo_carica = models.ForeignKey(OppTipoCarica)
    carica = models.CharField(max_length=30, blank=True)
    data_inizio = models.DateField(null=True, blank=True)
    data_fine = models.DateField(null=True, blank=True)
    legislatura = models.IntegerField(null=True, blank=True)
    circoscrizione = models.CharField(max_length=60, blank=True)
    presenze = models.IntegerField(null=True, blank=True)
    assenze = models.IntegerField(null=True, blank=True)
    missioni = models.IntegerField(null=True, blank=True)
    parliament_id = models.IntegerField(null=True, blank=True)
    indice = models.FloatField(null=True, blank=True)
    scaglione = models.IntegerField(null=True, blank=True)
    posizione = models.IntegerField(null=True, blank=True)
    media = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    ribelle = models.IntegerField(null=True, blank=True)
    maggioranza_sotto = models.IntegerField()
    maggioranza_sotto_assente = models.IntegerField()
    maggioranza_salva = models.IntegerField()
    maggioranza_salva_assente = models.IntegerField()
    class Meta:
        db_table = u'opp_carica'

class OppCaricaHasAtto(models.Model):
    atto = models.ForeignKey(OppAtto)
    carica = models.ForeignKey(OppCarica)
    tipo = models.CharField(max_length=255)
    data = models.DateField(null=True, blank=True)
    url = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    delete_at = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'opp_carica_has_atto'

class OppCaricaHasEmendamento(models.Model):
    emendamento = models.ForeignKey(OppEmendamento)
    carica = models.ForeignKey(OppCarica)
    tipo = models.CharField(max_length=255)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_carica_has_emendamento'

class OppCaricaHasGruppo(models.Model):
    carica = models.ForeignKey(OppCarica)
    gruppo = models.ForeignKey(OppGruppo)
    data_inizio = models.DateField(primary_key=True)
    data_fine = models.DateField(null=True, blank=True)
    ribelle = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    presenze = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_carica_has_gruppo'

class OppCaricaInterna(models.Model):
    id = models.IntegerField(primary_key=True)
    carica = models.ForeignKey(OppCarica)
    tipo_carica = models.ForeignKey(OppTipoCarica)
    sede = models.ForeignKey(OppSede)
    data_inizio = models.DateField(null=True, blank=True)
    data_fine = models.DateField(null=True, blank=True)
    descrizione = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_carica_interna'

class OppCategoria(models.Model):
    id = models.IntegerField(primary_key=True)
    denominazione = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_categoria'

class OppCategoriaHasTt(models.Model):
    categoria = models.ForeignKey(OppCategoria)
    teseott = models.ForeignKey(OppTeseott)
    class Meta:
        db_table = u'opp_categoria_has_tt'

class OppDocumento(models.Model):
    id = models.IntegerField(primary_key=True)
    atto = models.ForeignKey(OppAtto)
    data = models.DateField(null=True, blank=True)
    titolo = models.CharField(max_length=512, blank=True)
    testo = models.TextField(blank=True)
    file_pdf = models.TextField(blank=True)
    url_testo = models.CharField(max_length=1024, blank=True)
    url_pdf = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    dossier = models.IntegerField()
    class Meta:
        db_table = u'opp_documento'

class OppEmIter(models.Model):
    id = models.IntegerField(primary_key=True)
    fase = models.CharField(max_length=255, blank=True)
    concluso = models.IntegerField(null=True, blank=True)
    descrizione = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_em_iter'

class OppEmTesto(models.Model):
    id = models.IntegerField(primary_key=True)
    emendamento = models.ForeignKey(OppEmendamento)
    data = models.DateField(null=True, blank=True)
    testo = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    titolo = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_em_testo'

class OppEmendamento(models.Model):
    id = models.IntegerField(primary_key=True)
    titolo = models.CharField(max_length=255)
    numfase = models.CharField(max_length=255, blank=True)
    data_pres = models.DateField(null=True, blank=True)
    articolo = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    url_fonte = models.CharField(max_length=1024)
    sede = models.ForeignKey(OppSede)
    tipologia = models.CharField(max_length=255, blank=True)
    nota = models.CharField(max_length=255, blank=True)
    legislatura = models.IntegerField()
    titolo_aggiuntivo = models.TextField(blank=True)
    nb_commenti = models.IntegerField()
    ut_fav = models.IntegerField()
    ut_contr = models.IntegerField()
    class Meta:
        db_table = u'opp_emendamento'

class OppEmendamentoHasIter(models.Model):
    emendamento = models.ForeignKey(OppEmendamento)
    em_iter = models.ForeignKey(OppEmIter)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    nota = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_emendamento_has_iter'

class OppEsitoSeduta(models.Model):
    id = models.IntegerField(primary_key=True)
    atto = models.ForeignKey(OppAtto)
    sede = models.ForeignKey(OppSede)
    data = models.DateField(null=True, blank=True)
    url = models.TextField()
    esito = models.TextField(blank=True)
    tipologia = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_esito_seduta'

class OppGruppo(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, blank=True)
    acronimo = models.CharField(max_length=80, blank=True)
    class Meta:
        db_table = u'opp_gruppo'

class OppGruppoIsMaggioranza(models.Model):
    id = models.IntegerField(primary_key=True)
    gruppo = models.ForeignKey(OppGruppo)
    data_inizio = models.DateField()
    data_fine = models.DateField(null=True, blank=True)
    maggioranza = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_gruppo_is_maggioranza'

class OppGruppoRamo(models.Model):
    id = models.IntegerField(primary_key=True)
    gruppo = models.ForeignKey(OppGruppo)
    ramo = models.CharField(max_length=1, blank=True)
    data_inizio = models.DateField()
    data_fine = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'opp_gruppo_ramo'

class OppIntervento(models.Model):
    id = models.IntegerField(primary_key=True)
    atto = models.ForeignKey(OppAtto)
    carica = models.ForeignKey(OppCarica)
    tipologia = models.CharField(max_length=255, blank=True)
    url = models.TextField(blank=True)
    data = models.DateField(null=True, blank=True)
    sede = models.ForeignKey(OppSede)
    numero = models.IntegerField(null=True, blank=True)
    ap = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    ut_fav = models.IntegerField()
    ut_contr = models.IntegerField()
    class Meta:
        db_table = u'opp_intervento'

class OppIter(models.Model):
    id = models.IntegerField(primary_key=True)
    fase = models.CharField(max_length=255, blank=True)
    concluso = models.IntegerField(null=True, blank=True)
    cache_cod = models.CharField(max_length=6, blank=True)
    class Meta:
        db_table = u'opp_iter'

class OppLegge(models.Model):
    id = models.IntegerField(primary_key=True)
    atto = models.ForeignKey(OppAtto)
    numero = models.IntegerField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    url = models.TextField(blank=True)
    gu = models.TextField(blank=True)
    class Meta:
        db_table = u'opp_legge'

class OppLegislaturaHasGruppo(models.Model):
    legislatura = models.IntegerField()
    ramo = models.CharField(max_length=3)
    gruppo = models.ForeignKey(OppGruppo)
    class Meta:
        db_table = u'opp_legislatura_has_gruppo'

class OppPolicy(models.Model):
    id = models.IntegerField(primary_key=True)
    titolo = models.CharField(max_length=255, blank=True)
    descrizione = models.TextField(blank=True)
    provvisoria = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_policy'

class OppPolicyHasVotazione(models.Model):
    policy = models.ForeignKey(OppPolicy)
    votazione = models.ForeignKey(OppVotazione)
    voto = models.CharField(max_length=75, blank=True)
    strong = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_policy_has_votazione'

class OppPoliticianHistoryCache(models.Model):
    id = models.IntegerField(primary_key=True)
    legislatura = models.IntegerField(null=True, blank=True)
    data = models.DateField(unique=True)
    assenze = models.FloatField(null=True, blank=True)
    presenze = models.FloatField(null=True, blank=True)
    missioni = models.FloatField(null=True, blank=True)
    indice = models.FloatField(null=True, blank=True)
    ribellioni = models.FloatField(null=True, blank=True)
    chi_tipo = models.CharField(max_length=1, unique=True)
    chi_id = models.IntegerField()
    ramo = models.CharField(max_length=1, unique=True)
    numero = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    gruppo_id = models.IntegerField(null=True, blank=True)
    assenze_delta = models.FloatField(null=True, blank=True)
    presenze_delta = models.FloatField(null=True, blank=True)
    missioni_delta = models.FloatField(null=True, blank=True)
    indice_delta = models.FloatField(null=True, blank=True)
    ribellioni_delta = models.FloatField(null=True, blank=True)
    assenze_pos = models.IntegerField(null=True, blank=True)
    presenze_pos = models.IntegerField(null=True, blank=True)
    missioni_pos = models.IntegerField(null=True, blank=True)
    indice_pos = models.IntegerField(null=True, blank=True)
    ribellioni_pos = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_politician_history_cache'

class OppPolitico(models.Model):
    id = models.IntegerField()
    nome = models.CharField(max_length=30, blank=True)
    cognome = models.CharField(max_length=30, blank=True)
    n_monitoring_users = models.IntegerField()
    sesso = models.CharField(max_length=1, blank=True)
    class Meta:
        db_table = u'opp_politico'

class OppPremiumDemo(models.Model):
    id = models.IntegerField(primary_key=True)
    eta = models.IntegerField()
    attivita = models.IntegerField()
    attivita_aut_desc = models.CharField(max_length=255, blank=True)
    attivita_dip_desc = models.CharField(max_length=255, blank=True)
    attivita_amm_desc = models.CharField(max_length=255, blank=True)
    perche = models.IntegerField()
    perche_altro_desc = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(OppUser)
    class Meta:
        db_table = u'opp_premium_demo'

class OppRelazioneAtto(models.Model):
    id = models.IntegerField(primary_key=True)
    atto_from = models.ForeignKey(OppAtto)
    atto_to = models.ForeignKey(OppAtto)
    tipo_relazione = models.ForeignKey(OppTipoRelazione)
    descrizione = models.CharField(max_length=60, blank=True)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_relazione_atto'

class OppResoconto(models.Model):
    id = models.IntegerField(primary_key=True)
    sede = models.ForeignKey(OppSede)
    data = models.DateField(null=True, blank=True)
    comunicato = models.TextField(blank=True)
    sommario = models.TextField(blank=True)
    stenografico = models.TextField(blank=True)
    num_seduta = models.IntegerField(null=True, blank=True)
    legislatura = models.IntegerField()
    nota = models.TextField(blank=True)
    url_sommario = models.CharField(max_length=255, blank=True)
    url_stenografico = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    url_comunicato = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_resoconto'

class OppSede(models.Model):
    id = models.IntegerField(primary_key=True)
    codice = models.CharField(max_length=255, blank=True)
    ramo = models.CharField(max_length=255, blank=True)
    denominazione = models.CharField(max_length=255, blank=True)
    legislatura = models.IntegerField(null=True, blank=True)
    tipologia = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_sede'

class OppSeduta(models.Model):
    id = models.IntegerField(primary_key=True)
    data = models.DateField(null=True, blank=True)
    numero = models.IntegerField()
    ramo = models.CharField(max_length=3)
    legislatura = models.IntegerField()
    url = models.TextField(blank=True)
    is_imported = models.IntegerField()
    class Meta:
        db_table = u'opp_seduta'

class OppSimilarita(models.Model):
    carica_from = models.ForeignKey(OppCarica, primary_key=True)
    carica_to = models.ForeignKey(OppCarica)
    voting_similarity = models.FloatField()
    signing_similarity = models.FloatField()
    class Meta:
        db_table = u'opp_similarita'

class OppTagHasTt(models.Model):
    tag = models.ForeignKey(SfTag)
    teseott = models.ForeignKey(OppTeseott)
    class Meta:
        db_table = u'opp_tag_has_tt'

class OppTagHistoryCache(models.Model):
    id = models.IntegerField(primary_key=True)
    legislatura = models.IntegerField(null=True, blank=True)
    data = models.DateField(unique=True)
    indice = models.FloatField(null=True, blank=True)
    chi_tipo = models.CharField(max_length=1, unique=True)
    chi_id = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    indice_pos = models.IntegerField(null=True, blank=True)
    indice_delta = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'opp_tag_history_cache'

class OppTeseo(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_teseo = models.ForeignKey(OppTipoTeseo)
    denominazione = models.TextField(blank=True)
    ns_denominazione = models.TextField(blank=True)
    teseott_id = models.IntegerField(null=True, blank=True)
    tt = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_teseo'

class OppTeseoHasTeseott(models.Model):
    teseo = models.ForeignKey(OppTeseo)
    teseott = models.ForeignKey(OppTeseott)
    class Meta:
        db_table = u'opp_teseo_has_teseott'

class OppTeseoMapping(models.Model):
    id = models.IntegerField(primary_key=True)
    teseo_value = models.CharField(max_length=512, blank=True)
    tag = models.ForeignKey(SfTag, null=True, blank=True)
    class Meta:
        db_table = u'opp_teseo_mapping'

class OppTeseott(models.Model):
    id = models.IntegerField(primary_key=True)
    denominazione = models.TextField(blank=True)
    ns_denominazione = models.TextField(blank=True)
    teseo_senato = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_teseott'

class OppTipoAtto(models.Model):
    id = models.IntegerField(primary_key=True)
    denominazione = models.CharField(max_length=60, blank=True)
    descrizione = models.CharField(max_length=60, blank=True)
    spiegazione = models.TextField(blank=True)
    class Meta:
        db_table = u'opp_tipo_atto'

class OppTipoCarica(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_tipo_carica'

class OppTipoRelazione(models.Model):
    id = models.IntegerField(primary_key=True)
    denominazione = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'opp_tipo_relazione'

class OppTipoTeseo(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = u'opp_tipo_teseo'

class OppUser(models.Model):
    id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=16, blank=True)
    email = models.CharField(max_length=100)
    picture = models.TextField(blank=True)
    url_personal_website = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    has_paypal = models.IntegerField(null=True, blank=True)
    public_name = models.IntegerField()
    votes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    discussions = models.IntegerField(null=True, blank=True)
    last_contribution = models.DateTimeField(null=True, blank=True)
    n_monitored_objects = models.IntegerField(null=True, blank=True)
    n_monitored_tests = models.IntegerField(null=True, blank=True)
    n_monitored_tags = models.IntegerField(null=True, blank=True)
    n_monitored_attos = models.IntegerField(null=True, blank=True)
    n_monitored_politicos = models.IntegerField(null=True, blank=True)
    n_max_monitored_tags = models.IntegerField(null=True, blank=True)
    n_max_monitored_items = models.IntegerField(null=True, blank=True)
    wants_newsletter = models.IntegerField(null=True, blank=True)
    location_id = models.IntegerField(null=True, blank=True)
    is_active = models.IntegerField()
    last_alerted_at = models.DateTimeField(null=True, blank=True)
    n_alerts = models.IntegerField(null=True, blank=True)
    n_max_monitored_alerts = models.IntegerField(null=True, blank=True)
    is_premium = models.IntegerField(null=True, blank=True)
    is_adhoc = models.IntegerField(null=True, blank=True)
    wants_opp_news = models.IntegerField(null=True, blank=True)
    wants_opp_alerts = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'opp_user'

class OppVotazione(models.Model):
    id = models.IntegerField(primary_key=True)
    seduta = models.ForeignKey(OppSeduta)
    numero_votazione = models.IntegerField()
    titolo = models.TextField(blank=True)
    presenti = models.IntegerField(null=True, blank=True)
    votanti = models.IntegerField(null=True, blank=True)
    maggioranza = models.IntegerField(null=True, blank=True)
    astenuti = models.IntegerField(null=True, blank=True)
    favorevoli = models.IntegerField(null=True, blank=True)
    contrari = models.IntegerField(null=True, blank=True)
    esito = models.CharField(max_length=60, blank=True)
    ribelli = models.IntegerField(null=True, blank=True)
    margine = models.IntegerField(null=True, blank=True)
    tipologia = models.CharField(max_length=60, blank=True)
    descrizione = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=True)
    finale = models.IntegerField()
    nb_commenti = models.IntegerField()
    is_imported = models.IntegerField()
    titolo_aggiuntivo = models.TextField(blank=True)
    ut_fav = models.IntegerField()
    ut_contr = models.IntegerField()
    is_maggioranza_sotto_salva = models.IntegerField()
    class Meta:
        db_table = u'opp_votazione'

class OppVotazioneHasAtto(models.Model):
    votazione = models.ForeignKey(OppVotazione)
    atto = models.ForeignKey(OppAtto)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_votazione_has_atto'

class OppVotazioneHasCarica(models.Model):
    votazione = models.ForeignKey(OppVotazione)
    carica = models.ForeignKey(OppCarica)
    voto = models.CharField(max_length=40, blank=True)
    ribelle = models.IntegerField()
    maggioranza_sotto_salva = models.IntegerField()
    class Meta:
        db_table = u'opp_votazione_has_carica'

class OppVotazioneHasEmendamento(models.Model):
    votazione = models.ForeignKey(OppVotazione)
    emendamento = models.ForeignKey(OppEmendamento)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'opp_votazione_has_emendamento'

class OppVotazioneHasGruppo(models.Model):
    votazione = models.ForeignKey(OppVotazione)
    gruppo = models.ForeignKey(OppGruppo)
    voto = models.CharField(max_length=40, blank=True)
    class Meta:
        db_table = u'opp_votazione_has_gruppo'

class SfBlogComment(models.Model):
    id = models.IntegerField(primary_key=True)
    sf_blog_post = models.ForeignKey(SfBlogPost, null=True, blank=True)
    author_name = models.CharField(max_length=255, blank=True)
    author_email = models.CharField(max_length=255, blank=True)
    author_url = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    is_moderated = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_blog_comment'

class SfBlogPost(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(OppUser, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    stripped_title = models.CharField(max_length=255, unique=True, blank=True)
    extract = models.TextField(blank=True)
    content = models.TextField(blank=True)
    is_published = models.IntegerField(null=True, blank=True)
    allow_comments = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateField(unique=True, null=True, blank=True)
    class Meta:
        db_table = u'sf_blog_post'

class SfBlogTag(models.Model):
    sf_blog_post = models.ForeignKey(SfBlogPost, primary_key=True)
    tag = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_blog_tag'

class SfBookmarkings(models.Model):
    id = models.IntegerField(primary_key=True)
    bookmarkable_model = models.CharField(max_length=50)
    bookmarkable_id = models.IntegerField()
    user_id = models.IntegerField(null=True, blank=True)
    bookmarking = models.IntegerField()
    class Meta:
        db_table = u'sf_bookmarkings'

class SfComment(models.Model):
    id = models.IntegerField(primary_key=True)
    commentable_model = models.CharField(max_length=30, blank=True)
    commentable_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)
    author_id = models.IntegerField(null=True, blank=True)
    author_name = models.CharField(max_length=50, blank=True)
    author_email = models.CharField(max_length=100, blank=True)
    author_website = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    is_public = models.IntegerField()
    comment_namespace = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = u'sf_comment'

class SfCommunityNewsCache(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(null=True, blank=True)
    generator_model = models.CharField(max_length=50)
    generator_primary_keys = models.CharField(max_length=512, blank=True)
    related_model = models.CharField(max_length=50)
    related_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=128, blank=True)
    type = models.CharField(max_length=1, blank=True)
    vote = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'sf_community_news_cache'

class SfEmendComment(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=255)
    selection = models.TextField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
    author_id = models.IntegerField(null=True, blank=True)
    author_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    is_public = models.IntegerField()
    class Meta:
        db_table = u'sf_emend_comment'

class SfEmendLog(models.Model):
    id = models.IntegerField(primary_key=True)
    msg_type = models.CharField(max_length=30, blank=True)
    msg = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_emend_log'

class SfLaunching(models.Model):
    id = models.IntegerField(primary_key=True)
    object_model = models.CharField(max_length=50, unique=True)
    object_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(unique=True)
    launch_namespace = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = u'sf_launching'

class SfMonitoring(models.Model):
    id = models.IntegerField(primary_key=True)
    monitorable_model = models.CharField(max_length=50)
    monitorable_id = models.IntegerField()
    user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_monitoring'

class SfNewsCache(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(null=True, blank=True)
    generator_model = models.CharField(max_length=50)
    related_monitorable_model = models.CharField(max_length=50)
    related_monitorable_id = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField()
    generator_primary_keys = models.CharField(max_length=512, blank=True)
    data_presentazione_atto = models.DateTimeField(null=True, blank=True)
    ramo_votazione = models.CharField(max_length=1, blank=True)
    sede_intervento_id = models.IntegerField(null=True, blank=True)
    tipo_atto_id = models.IntegerField(null=True, blank=True)
    succ = models.IntegerField(null=True, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'sf_news_cache'

class SfPriority(models.Model):
    id = models.IntegerField(primary_key=True)
    prioritisable_model = models.CharField(max_length=50)
    prioritisable_id = models.IntegerField()
    user_id = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_priority'

class SfRatings(models.Model):
    id = models.IntegerField(primary_key=True)
    ratable_model = models.CharField(max_length=50)
    ratable_id = models.IntegerField()
    user_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField()
    class Meta:
        db_table = u'sf_ratings'

class SfTag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=True)
    is_triple = models.IntegerField(null=True, blank=True)
    triple_namespace = models.CharField(max_length=100, blank=True)
    triple_key = models.CharField(max_length=100, blank=True)
    triple_value = models.CharField(max_length=255, blank=True)
    is_tmp = models.IntegerField()
    n_monitoring_users = models.IntegerField()
    class Meta:
        db_table = u'sf_tag'

class SfTagging(models.Model):
    id = models.IntegerField(primary_key=True)
    tag = models.ForeignKey(SfTag)
    taggable_model = models.CharField(max_length=30, blank=True)
    taggable_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_tagging'

class SfTaggingForIndex(models.Model):
    tag = models.ForeignKey(SfTag, primary_key=True)
    atto = models.ForeignKey(OppAtto)
    user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'sf_tagging_for_index'


"""