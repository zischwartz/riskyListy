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



class UserAdmin(admin.ModelAdmin):
	list_display = ("name",)
	ordering = ("name",)
	search_fields = ("name",)

admin.site.register(models.User, UserAdmin)



class TeamAdmin(admin.ModelAdmin):
	list_display = ("user", "name")
	ordering = ("user",)
	search_fields = ("user",)

admin.site.register(models.Team, TeamAdmin)



class PlayerAdmin(admin.ModelAdmin):
	list_display = ("emailer", "team", "points")
	list_filter = ("team",)
	ordering = ("team", "emailer")
	search = ("team", "emailer")

admin.site.register(models.Player, PlayerAdmin)



class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "total")

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

