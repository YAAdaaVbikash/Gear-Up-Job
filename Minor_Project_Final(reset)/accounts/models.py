from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# from django.contrib.postgres.fields import ArrayField



# Create your models here.
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


def user_directory_path(instance, filename):
    return 'Company/user_{0}_{1}/{2}'.format(instance.company_username.id, instance.company_username, filename)


class Company(models.Model):
    company_username = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    url = models.URLField(max_length=200, blank=False)
    profile_pic = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True,)
    background_image = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True,)
    phone_number = models.CharField(max_length=50, unique=True, blank=False)
    is_company = models.BooleanField(default=True, editable=False)
    is_jobseeker = models.BooleanField(default=False, editable=False)
    Total_Jobs = models.PositiveIntegerField(default=0)
    Total_Views = models.PositiveIntegerField(default=0)

    total_rating=models.PositiveIntegerField(default=0)
    number_of_rating = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)


    def update_rating(self,value):
        self.total_rating = self.total_rating + value
        self.save()
        self.number_of_rating = self.number_of_rating + 1
        self.save()
        self.rating = self.total_rating / self.number_of_rating
        self.save()

    def activated_company(self):
        pass

    def update_views(self):
        self.Total_Views = self.Total_Views + 1
        self.save()

    def update_jobs(self):
        self.Total_Jobs = self.jobs.all().count()

    def __str__(self):
        return self.company_username.username


class Seeker(models.Model):
    JOB_CATAGORIES = (
        ('Academic librarian','Academic librarian'),
        ('Accountant','Accountant'),
        ('Accounting technician','Accounting technician'),
        ('Actor','Actor'),
        ('Actuary','Actuary'),
        ('Administrative Assistant/Secretary','Administrative Assistant/Secretary'),
        ('Adult nurse','Adult nurse'),
        ('Advertising','Advertising'),
        ('Advertising account executive','Advertising account executive'),
        ('Advertising account planner','Advertising account planner'),
        ('Advertising copywriter','Advertising copywriter'),
        ('Advice worker','Advice worker'),
        ('Advocate (Scotland)','Advocate (Scotland)'),
        ('Aeronautical engineer','Aeronautical engineer'),
        ('Agricultural consultant','Agricultural consultant'),
        ('Agricultural manager','Agricultural manager'),
        ('Aid worker/humanitarian worker','Aid worker/humanitarian worker'),
        ('Air traffic controller','Air traffic controller'),
        ('Aircraft Mechanic','Aircraft Mechanic'),
        ('Airline cabin crew','Airline cabin crew'),
        ('Airline Pilot','Airline Pilot'),
        ('Amenity horticulturist','Amenity horticulturist'),
        ('Analytical chemist','Analytical chemist'),
        ('Animal Careers','Animal Careers'),
        ('Animal nutritionist','Animal nutritionist'),
        ('Animator','Animator'),
        ('Archaeologist','Archaeologist'),
        ('Architect','Architect'),
        ('Architectural technologist','Architectural technologist'),
        ('Archivist','Archivist'),
        ('Armed forces officer','Armed forces officer'),
        ('Aromatherapist','Aromatherapist'),
        ('Art Appraiser','Art Appraiser'),
        ('Art Auctioneer','Art Auctioneer'),
        ('Art therapist','Art therapist'),
        ('Artist','Artist'),
        ('Arts administrator','Arts administrator'),
        ('Auditor','Auditor'),
        ('Automotive engineer','Automotive engineer'),
        ('Back End Developer','Back End Developer'),
        ('Bank Teller','Bank Teller'),
        ('Barrister','Barrister'),
        ('BarristerÎ“Ã‡Ã–s clerk','BarristerÎ“Ã‡Ã–s clerk'),
        ('Bid manager','Bid manager'),
        ('Bilingual secretary','Bilingual secretary'),
        ('Biomedical engineer','Biomedical engineer'),
        ('Biomedical scientist','Biomedical scientist'),
        ('Biotechnologist','Biotechnologist'),
        ('Book Publishing','Book Publishing'),
        ('Border Control Agent','Border Control Agent'),
        ('Border force officer','Border force officer'),
        ('Brand manager','Brand manager'),
        ('Broadcasting presenter','Broadcasting presenter'),
        ('Building control officer/surveyor','Building control officer/surveyor'),
        ('Building services engineer','Building services engineer'),
        ('Building surveyor','Building surveyor'),
        ('Business analyst','Business analyst'),
        ('Call Center','Call Center'),
        ('Camera operator','Camera operator'),
        ('Careers adviser','Careers adviser'),
        ('Careers adviser (higher education)','Careers adviser (higher education)'),
        ('Careers consultant','Careers consultant'),
        ('Cartographer','Cartographer'),
        ('Catering manager','Catering manager'),
        ('Charities administrator','Charities administrator'),
        ('Charities fundraiser','Charities fundraiser'),
        ('Chemical (process) engineer','Chemical (process) engineer'),
        ('Chief Operating Officer','Chief Operating Officer'),
        ('Child psychotherapist','Child psychotherapist'),
        ('Chiropractor','Chiropractor'),
        ('City Manager','City Manager'),
        ('Civil engineer','Civil engineer'),
        ('Civil Service administrator','Civil Service administrator'),
        ('Clinical biochemist','Clinical biochemist'),
        ('Clinical cytogeneticist','Clinical cytogeneticist'),
        ('Clinical microbiologist','Clinical microbiologist'),
        ('Clinical molecular geneticist','Clinical molecular geneticist'),
        ('Clinical research associate','Clinical research associate'),
        ('Clinical scientist - tissue typing','Clinical scientist - tissue typing'),
        ('Clothing and textile technologist','Clothing and textile technologist'),
        ('College Professor','College Professor'),
        ('Colour technologist','Colour technologist'),
        ('Commercial airline pilot','Commercial airline pilot'),
        ('Commercial horticulturist','Commercial horticulturist'),
        ('Commercial/residential/rural surveyor','Commercial/residential/rural surveyor'),
        ('Commissioning editor','Commissioning editor'),
        ('Commissioning engineer','Commissioning engineer'),
        ('Commodity broker','Commodity broker'),
        ('Communications engineer','Communications engineer'),
        ('Community arts worker','Community arts worker'),
        ('Community education officer','Community education officer'),
        ('Community worker','Community worker'),
        ('Company secretary','Company secretary'),
        ('Computer Programmer','Computer Programmer'),
        ('Computer sales support','Computer sales support'),
        ('Computer scientist','Computer scientist'),
        ('Computer Systems Administrator','Computer Systems Administrator'),
        ('Conference organiser','Conference organiser'),
        ('Consultant','Consultant'),
        ('Control and instrumentation engineer','Control and instrumentation engineer'),
        ('Corporate banker','Corporate banker'),
        ('Corporate treasurer','Corporate treasurer'),
        ('Correctional Officer','Correctional Officer'),
        ('Counsellor','Counsellor'),
        ('Court reporter/verbatim reporter','Court reporter/verbatim reporter'),
        ('Credit analyst','Credit analyst'),
        ('Criminal Justice','Criminal Justice'),
        ('Crown Prosecution Service lawyer','Crown Prosecution Service lawyer'),
        ('Crystallographer','Crystallographer'),
        ('Curator','Curator'),
        ('Customs officer','Customs officer'),
        ('Cyber security specialist','Cyber security specialist'),
        ('Dance movement psychotherapist','Dance movement psychotherapist'),
        ('Data analyst','Data analyst'),
        ('Data scientist','Data scientist'),
        ('Data visualisation analyst','Data visualisation analyst'),
        ('Database administrator','Database administrator'),
        ('Database Administrator','Database Administrator'),
        ('DCIS Special Agent','DCIS Special Agent'),
        ('Debt/finance adviser','Debt/finance adviser'),
        ('Dental hygienist','Dental hygienist'),
        ('Dentist','Dentist'),
        ('Design engineer','Design engineer'),
        ('Design manager (construction)','Design manager (construction)'),
        ('DevOps engineer','DevOps engineer'),
        ('Dietitian','Dietitian'),
        ('Diplomatic service','Diplomatic service'),
        ('Doctor (general practitioner, GP)','Doctor (general practitioner, GP)'),
        ('Doctor (hospital)','Doctor (hospital)'),
        ('Dramatherapist','Dramatherapist'),
        ('Economist','Economist'),
        ('Editorial assistant','Editorial assistant'),
        ('Education administrator','Education administrator'),
        ('Electrical engineer','Electrical engineer'),
        ('Electronics engineer','Electronics engineer'),
        ('Energy conservation officer','Energy conservation officer'),
        ('Energy consultant','Energy consultant'),
        ('Engineering geologist','Engineering geologist'),
        ('Environmental education officer','Environmental education officer'),
        ('Environmental health officer','Environmental health officer'),
        ('Environmental manager','Environmental manager'),
        ('Environmental scientist','Environmental scientist'),
        ('Equal opportunities officer','Equal opportunities officer'),
        ('Equality and diversity officer','Equality and diversity officer'),
        ('Ergonomist','Ergonomist'),
        ('Estate agent','Estate agent'),
        ('Estimator','Estimator'),
        ('Exhibition display designer','Exhibition display designer'),
        ('Exhibition organiser','Exhibition organiser'),
        ('Exploration geologist','Exploration geologist'),
        ('Facilities manager','Facilities manager'),
        ('FBI Special Agent','FBI Special Agent'),
        ('Federal Air Marshall','Federal Air Marshall'),
        ('Federal Law Enforcement','Federal Law Enforcement'),
        ('Field trials officer','Field trials officer'),
        ('Financial Advisor','Financial Advisor'),
        ('Financial manager','Financial manager'),
        ('Fire engineer','Fire engineer'),
        ('Firefighter','Firefighter'),
        ('Fish and Game Warden','Fish and Game Warden'),
        ('Fisheries enforcement officer','Fisheries enforcement officer'),
        ('Fitness centre manager','Fitness centre manager'),
        ('Flight Attendant','Flight Attendant'),
        ('Food scientist','Food scientist'),
        ('Food technologist','Food technologist'),
        ('Forensic Psychologist','Forensic Psychologist'),
        ('Forensic scientist','Forensic scientist'),
        ('Freelance Writer','Freelance Writer'),
        ('Freight forwarder','Freight forwarder'),
        ('Fundraiser','Fundraiser'),
        ('Geneticist','Geneticist'),
        ('Geographical information systems manager','Geographical information systems manager'),
        ('Geomatics/land surveyor','Geomatics/land surveyor'),
        ('Government Jobs','Government Jobs'),
        ('Government lawyer','Government lawyer'),
        ('Government research officer','Government research officer'),
        ('Graphic designer','Graphic designer'),
        ('Hair Stylist','Hair Stylist'),
        ('Health and safety adviser','Health and safety adviser'),
        ('Health and safety inspector','Health and safety inspector'),
        ('Health promotion specialist','Health promotion specialist'),
        ('Health service manager','Health service manager'),
        ('Health visitor','Health visitor'),
        ('Herbalist','Herbalist'),
        ('Heritage manager','Heritage manager'),
        ('Higher education administrator','Higher education administrator'),
        ('Higher education advice worker','Higher education advice worker'),
        ('Homeless support worker','Homeless support worker'),
        ('Horticultural consultant','Horticultural consultant'),
        ('Hospitalist','Hospitalist'),
        ('Hotel manager','Hotel manager'),
        ('Housing adviser','Housing adviser'),
        ('Human Resources','Human Resources'),
        ('Human resources officer','Human resources officer'),
        ('Hydrologist','Hydrologist'),
        ('ICE Agent','ICE Agent'),
        ('Illustrator','Illustrator'),
        ('Immigration officer','Immigration officer'),
        ('Immunologist','Immunologist'),
        ('Industrial/product designer','Industrial/product designer'),
        ('Information scientist','Information scientist'),
        ('Information systems manager','Information systems manager'),
        ('Information technology/software trainers','Information technology/software trainers'),
        ('Insurance Agent','Insurance Agent'),
        ('Insurance broker','Insurance broker'),
        ('Insurance claims inspector','Insurance claims inspector'),
        ('Insurance risk surveyor','Insurance risk surveyor'),
        ('Insurance underwriter','Insurance underwriter'),
        ('Interpreter','Interpreter'),
        ('Investment analyst','Investment analyst'),
        ('Investment Banker','Investment Banker'),
        ('Investment banker - corporate finance','Investment banker - corporate finance'),
        ('Investment banker Î“Ã‡Ã´ operations','Investment banker Î“Ã‡Ã´ operations'),
        ('Investment fund manager','Investment fund manager'),
        ('IT consultant','IT consultant'),
        ('IT support analyst','IT support analyst'),
        ('Journalist','Journalist'),
        ('K-9 Police Officer','K-9 Police Officer'),
        ('Laboratory technician','Laboratory technician'),
        ('Land-based engineer','Land-based engineer'),
        ('Landscape architect','Landscape architect'),
        ('Lawyer','Lawyer'),
        ('Learning disability nurse','Learning disability nurse'),
        ('Learning mentor','Learning mentor'),
        ('Lecturer (adult education)','Lecturer (adult education)'),
        ('Lecturer (further education)','Lecturer (further education)'),
        ('Lecturer (higher education)','Lecturer (higher education)'),
        ('Legal executive','Legal executive'),
        ('Leisure centre manager','Leisure centre manager'),
        ('Licensed conveyancer','Licensed conveyancer'),
        ('Local government administrator','Local government administrator'),
        ('Local government lawyer','Local government lawyer'),
        ('Logistics/distribution manager','Logistics/distribution manager'),
        ('Magazine features editor','Magazine features editor'),
        ('Magazine journalist','Magazine journalist'),
        ('Maintenance engineer','Maintenance engineer'),
        ('Management','Management'),
        ('Management accountant','Management accountant'),
        ('Manufacturing engineer','Manufacturing engineer'),
        ('Manufacturing machine operator','Manufacturing machine operator'),
        ('Manufacturing toolmaker','Manufacturing toolmaker'),
        ('Marine scientist','Marine scientist'),
        ('Market research analyst','Market research analyst'),
        ('Market Research Analyst','Market Research Analyst'),
        ('Market research executive','Market research executive'),
        ('Marketing assistant','Marketing assistant'),
        ('Marketing executive','Marketing executive'),
        ('Marketing manager (direct)','Marketing manager (direct)'),
        ('Marketing manager (social media)','Marketing manager (social media)'),
        ('Materials engineer','Materials engineer'),
        ('Materials specialist','Materials specialist'),
        ('Mechanical engineer','Mechanical engineer'),
        ('Media analyst','Media analyst'),
        ('Media buyer','Media buyer'),
        ('Media planner','Media planner'),
        ('Medical physicist','Medical physicist'),
        ('Medical representative','Medical representative'),
        ('Mental Health Counselor','Mental Health Counselor'),
        ('Mental health nurse','Mental health nurse'),
        ('Metallurgist','Metallurgist'),
        ('Meteorologist','Meteorologist'),
        ('Microbiologist','Microbiologist'),
        ('Midwife','Midwife'),
        ('Military Careers','Military Careers'),
        ('Mining engineer','Mining engineer'),
        ('Mobile developer','Mobile developer'),
        ('Multimedia programmer','Multimedia programmer'),
        ('Multimedia specialists','Multimedia specialists'),
        ('Museum education officer','Museum education officer'),
        ('Museum Jobs','Museum Jobs'),
        ('Museum/gallery exhibition officer','Museum/gallery exhibition officer'),
        ('Music Conductor','Music Conductor'),
        ('Music Teacher','Music Teacher'),
        ('Music therapist','Music therapist'),
        ('Nanoscientist','Nanoscientist'),
        ('Nature conservation officer','Nature conservation officer'),
        ('Naval architect','Naval architect'),
        ('Network administrator','Network administrator'),
        ('Nurse','Nurse'),
        ('Nutritional therapist','Nutritional therapist'),
        ('Nutritionist','Nutritionist'),
        ('Occupational therapist','Occupational therapist'),
        ('Oceanographer','Oceanographer'),
        ('Office manager','Office manager'),
        ('Operational researcher','Operational researcher'),
        ('Orthodontist','Orthodontist'),
        ('Orthoptist','Orthoptist'),
        ('Outdoor pursuits manager','Outdoor pursuits manager'),
        ('Packaging technologist','Packaging technologist'),
        ('Paramedic','Paramedic'),
        ('Patent attorney','Patent attorney'),
        ('Patent examiner','Patent examiner'),
        ('Pediatrician','Pediatrician'),
        ('Pension scheme manager','Pension scheme manager'),
        ('Personal assistant','Personal assistant'),
        ('Personal Fitness Trainer','Personal Fitness Trainer'),
        ('Petroleum engineer','Petroleum engineer'),
        ('Pharmacist','Pharmacist'),
        ('Pharmacologist','Pharmacologist'),
        ('Pharmacovigilance officer','Pharmacovigilance officer'),
        ('Photographer','Photographer'),
        ('Physician Assistant','Physician Assistant'),
        ('Physiotherapist','Physiotherapist'),
        ('Picture researcher','Picture researcher'),
        ('Planning and development surveyor','Planning and development surveyor'),
        ('Planning technician','Planning technician'),
        ('Plant breeder','Plant breeder'),
        ('Police Dispatcher','Police Dispatcher'),
        ('Police Officer','Police Officer'),
        ('Political party agent','Political party agent'),
        ('Political researcher','Political researcher'),
        ('Practice nurse','Practice nurse'),
        ('Press photographer','Press photographer'),
        ('Press sub-editor','Press sub-editor'),
        ('Prison officer','Prison officer'),
        ('Private music teacher','Private music teacher'),
        ('Probation officer','Probation officer'),
        ('Product development scientist','Product development scientist'),
        ('Production manager','Production manager'),
        ('Programme researcher','Programme researcher'),
        ('Programmer','Programmer'),
        ('Project manager','Project manager'),
        ('Psychiatrist','Psychiatrist'),
        ('Psychologist (clinical)s','Psychologist (clinical)s'),
        ('Psychologist (educational)','Psychologist (educational)'),
        ('Psychotherapist','Psychotherapist'),
        ('Public affairs consultant (lobbyist)','Public affairs consultant (lobbyist)'),
        ('Public affairs consultant (research)','Public affairs consultant (research)'),
        ('Public house manager','Public house manager'),
        ('Public librarian','Public librarian'),
        ('Public Relations','Public Relations'),
        ('Public relations (PR) officer','Public relations (PR) officer'),
        ('QA analyst','QA analyst'),
        ('Quality assurance manager','Quality assurance manager'),
        ('Quantity surveyor','Quantity surveyor'),
        ('Records manager','Records manager'),
        ('Recruitment consultant','Recruitment consultant'),
        ('Recycling officer','Recycling officer'),
        ('Regulatory affairs officer','Regulatory affairs officer'),
        ('Research chemist','Research chemist'),
        ('Research scientist','Research scientist'),
        ('Restaurant manager','Restaurant manager'),
        ('Retail','Retail'),
        ('Retail banker','Retail banker'),
        ('Retail buyer','Retail buyer'),
        ('Retail manager','Retail manager'),
        ('Retail merchandiser','Retail merchandiser'),
        ('Retail pharmacist','Retail pharmacist'),
        ('Sales','Sales'),
        ('Sales executive','Sales executive'),
        ('Scene of crime officer','Scene of crime officer'),
        ('School Jobs','School Jobs'),
        ('Secretary','Secretary'),
        ('Seismic interpreter','Seismic interpreter'),
        ('Site engineer','Site engineer'),
        ('Site manager','Site manager'),
        ('Social researcher','Social researcher'),
        ('Social worker','Social worker'),
        ('Software Developer','Software Developer'),
        ('Software engineer','Software engineer'),
        ('Soil scientist','Soil scientist'),
        ('Solicitor','Solicitor'),
        ('Speech and language therapist','Speech and language therapist'),
        ('Sports coach','Sports coach'),
        ('Sports development officer','Sports development officer'),
        ('Sports therapist','Sports therapist'),
        ('State Trooper','State Trooper'),
        ('Statistician','Statistician'),
        ('STEM CareersGeeks','STEM CareersGeeks'),
        ('Stockbroker','Stockbroker'),
        ('Structural engineer','Structural engineer'),
        ('Substitute Teacher','Substitute Teacher'),
        ('Systems analyst','Systems analyst'),
        ('Systems developer','Systems developer'),
        ('Tax inspector','Tax inspector'),
        ('Teacher','Teacher'),
        ('Teacher (nursery/early years)','Teacher (nursery/early years)'),
        ('Teacher (primary)','Teacher (primary)'),
        ('Teacher (secondary)','Teacher (secondary)'),
        ('Teacher (special educational needs)','Teacher (special educational needs)'),
        ('Teaching Abroad','Teaching Abroad'),
        ('Teaching Online','Teaching Online'),
        ('Teaching/classroom assistant','Teaching/classroom assistant'),
        ('Technical author','Technical author'),
        ('Technical sales engineer','Technical sales engineer'),
        ('TEFL/TESL teacher','TEFL/TESL teacher'),
        ('Television production assistant','Television production assistant'),
        ('Test automation developer','Test automation developer'),
        ('Tour guide','Tour guide'),
        ('Tour operator','Tour operator'),
        ('Tour/holiday representative','Tour/holiday representative'),
        ('Tourism officer','Tourism officer'),
        ('Tourist information manager','Tourist information manager'),
        ('Town and country planner','Town and country planner'),
        ('Toxicologist','Toxicologist'),
        ('Trade union official','Trade union official'),
        ('Trade union research officer','Trade union research officer'),
        ('Trader','Trader'),
        ('Trading standards officer','Trading standards officer'),
        ('Training and development officer','Training and development officer'),
        ('Translator','Translator'),
        ('Transportation planner','Transportation planner'),
        ('Transportation Security Officer','Transportation Security Officer'),
        ('Travel agent','Travel agent'),
        ('TV/film/theatre set designer','TV/film/theatre set designer'),
        ('Uniformed Secret Service Officer','Uniformed Secret Service Officer'),
        ('UX designer','UX designer'),
        ('Validation engineer','Validation engineer'),
        ('Veterinarian','Veterinarian'),
        ('Veterinary nurse','Veterinary nurse'),
        ('Veterinary surgeon','Veterinary surgeon'),
        ('Video game designer','Video game designer'),
        ('Video game developer','Video game developer'),
        ('Volunteer work organiser','Volunteer work organiser'),
        ('Waiter','Waiter'),
        ('Warehouse manager','Warehouse manager'),
        ('Waste management officer','Waste management officer'),
        ('Water conservation officer','Water conservation officer'),
        ('Water engineer','Water engineer'),
        ('Web designer','Web designer'),
        ('Web Developer','Web Developer'),
        ('Wedding Planner','Wedding Planner'),
        ('Welfare rights adviser','Welfare rights adviser'),
        ('Writer','Writer'),
        ('Writer/Editor','Writer/Editor'),
        ('Youth worker','Youth worker'),
    )

    seeker = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='seeker')
    full_name      = models.CharField(max_length=100, blank=False)
    job_category = models.CharField(choices=JOB_CATAGORIES,max_length=100, blank=False)
    job_category_1 = models.CharField(choices=JOB_CATAGORIES,max_length=100,null=True,blank=True)
    job_category_2 = models.CharField(choices=JOB_CATAGORIES,max_length=100,null=True,blank=True)
    job_category_3 = models.CharField(choices=JOB_CATAGORIES,max_length=100,null=True,blank=True)
    job_category_4 = models.CharField(choices=JOB_CATAGORIES,max_length=100,null=True,blank=True)

    not_rated          = models.BooleanField(default=True)

    history_0 = models.CharField(max_length=100,null=True,blank=True)
    history_1 = models.CharField(max_length=100,null=True,blank=True)
    history_2 = models.CharField(max_length=100,null=True,blank=True)
    history_3 = models.CharField(max_length=100,null=True,blank=True)
    history_4 = models.CharField(max_length=100,null=True,blank=True)
    history_5 = models.CharField(max_length=100,null=True,blank=True)
    history_6 = models.CharField(max_length=100,null=True,blank=True)
    history_7 = models.CharField(max_length=100,null=True,blank=True)
    history_8 = models.CharField(max_length=100,null=True,blank=True)
    history_9 = models.CharField(max_length=100,null=True,blank=True)
    history_10 = models.CharField(max_length=100,null=True,blank=True)
    history_11 = models.CharField(max_length=100,null=True,blank=True)
    history_12 = models.CharField(max_length=100,null=True,blank=True)
    history_13 = models.CharField(max_length=100,null=True,blank=True)
    history_14 = models.CharField(max_length=100,null=True,blank=True)
    is_company = models.BooleanField(default=False, editable=False)
    is_jobseeker = models.BooleanField(default=True, editable=False)


    def rated(self):
        self.not_rated = False
        self.save()
    def __str__(self):
        return self.seeker.username
    def add_history(self,title):
        self.history_14 = self.history_13
        self.save()
        self.history_13 = self.history_12
        self.save()
        self.history_12 = self.history_11
        self.save()
        self.history_11 = self.history_10
        self.save()
        self.history_10 = self.history_9
        self.save()
        self.history_9 = self.history_8
        self.save()
        self.history_8 = self.history_7
        self.save()
        self.history_7 = self.history_6
        self.save()
        self.history_6 = self.history_5
        self.save()
        self.history_5 = self.history_4
        self.save()
        self.history_4 = self.history_3
        self.save()
        self.history_3 = self.history_2
        self.save()
        self.history_2 = self.history_1
        self.save()
        self.history_1 = self.history_0
        self.save()
        self.history_0 = title
        self.save()
class Rating(models.Model):
    seeker_pk = models.ForeignKey(
        Seeker, on_delete=models.CASCADE, related_name='rating')
    company_pk = models.PositiveIntegerField(blank=True ,null = True)

    def save_pk(self,pk):
        self.company_pk =pk
        self.save()

    def __str__(self):
        return self.seeker_pk.full_name
