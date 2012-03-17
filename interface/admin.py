import models
from django.contrib import admin

class EmailerAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_display_links = ("name",)
	ordering = ("name",)

admin.site.register(models.Emailer, EmailerAdmin)



class EmailAddressAdmin(admin.ModelAdmin):
	list_display = ("emailer", "emailAddress")
	ordering = ("emailer",)
	search_fields = ("emailer", "emailAddress")

admin.site.register(models.EmailAddress, EmailAddressAdmin)



class TeamAdmin(admin.ModelAdmin):
	list_display = ("manager", "name")
	ordering = ("manager",)
	search_fields = ("manager",)

admin.site.register(models.Team, TeamAdmin)



class PlayerAdmin(admin.ModelAdmin):
	list_display = ("player", "team", "points")
	list_filter = ("team",)
	ordering = ("team", "player")
	search = ("team", "player")

admin.site.register(models.Player, PlayerAdmin)



class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)

admin.site.register(models.Category, CategoryAdmin)



class EmailerPointRankingAdmin(admin.ModelAdmin):
	list_display = ("emailer", "category", "type", "points")
	list_filter = ("type",)
	ordering = ("emailer", "category", "type")
	search = ("emailer", "category", "type")

admin.site.register(models.EmailerPointRanking, EmailerPointRankingAdmin)



class TeamPointRankingAdmin(admin.ModelAdmin):
	list_display = ("team", "category", "type", "points")
	list_filter = ("type",)
	ordering = ("team", "category", "type")
	search = ("team", "category", "type")

admin.site.register(models.TeamPointRanking, TeamPointRankingAdmin)

