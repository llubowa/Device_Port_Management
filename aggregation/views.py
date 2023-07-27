from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import AggregationHubs,AggregationIps,CascAggIps,CascadedHubs,CascadedIps



# Create your views here.
def agg(hub):
			value = AggregationIps.objects.get(hub_name=hub)
			ip =  value.ip_address
			name = value.hub_name
			result = [ip,name]
			return result

def casc(cascade,ip):
			value = CascAggIps.objects.get(cascade_no=cascade,agg_ip=ip)
			ip = value.ip_address
			name = value.cascaded
			result = [ip,name]
			return result
def return_name(ip):
	try:
		value = AggregationIps.objects.get(ip_address=ip)
		name = value.hub_name
		return name[16:]
	except:
		value = CascadedIps.objects.get(ip_address=ip)
		name = value.cascaded
		return name[7:]
	
def with_names(list):
	try:
		for val in list:
					site_name = return_name(val['ip_address'])
					val['ip_address'] = site_name
		return list
	except:
		for val in list:
					site_name = return_name(val.ip_address)
					val.ip_address = site_name
		return list
	
	

@login_required
def aggregation (request):
	if request.method =='POST':
		
		agg_hub = request.POST['AggregationHub']
		cascaded = request.POST['casc']
		status = request.POST['status']
		
		if agg_hub =='':
			name = f'You must Enter an aggregation site'
			return render(request,'aggregation/hubs.html',{'site':name})
		else:
			pass

		if cascaded == 'none' and status != 'all':
			hub = agg(agg_hub)
			ip = hub[0]
			name = hub[1]
			ports = AggregationHubs.objects.filter(ip_address=ip,status=status).exclude(port='A/1')
			result = with_names(ports)
			count = ports.count()
			return render(request,'aggregation/hubs.html',{'results':result,'site':name, 'counter':count,'selected_option':agg_hub,'status_option':status})
		elif cascaded =='none' and status == 'all':
			hub = agg(agg_hub)
			ip = hub[0]
			name = hub[1]
			ports = AggregationHubs.objects.filter(ip_address=ip).exclude(port='A/1')
			result = with_names(ports)
			count = ports.count()
			return render(request,'aggregation/hubs.html',{'results':result,'site':name,'counter':count,'selected_option':agg_hub,'status_option':status})
		elif cascaded != 'none'and status == 'all':
			try:
				aggip = agg(agg_hub)
				hub = casc(cascaded,aggip[0])
				ip = hub[0]
				name = hub[1]
				ports = CascadedHubs.objects.filter(ip_address=ip).exclude(description='10/100/Gig Ethernet TX')
				result = with_names(ports)
				count = ports.count()
				return render(request,'aggregation/hubs.html',{'results':result,'site':name,'counter':count,'selected_option':agg_hub,'cascaded_option':cascaded,'status_option':status})
			except:
				name = f'{agg_hub} has NO {cascaded}'
				return render(request,'aggregation/hubs.html',{'site':name,'selected_option':agg_hub,'cascaded_option':cascaded,'status_option':status})

		elif cascaded != 'none' and status != 'all':
			try:
				aggip = agg(agg_hub)
				hub = casc(cascaded,aggip[0])
				ip = hub[0]
				name = hub[1]
				ports = CascadedHubs.objects.filter(ip_address=ip,status=status).exclude(description='10/100/Gig Ethernet TX')
				result = with_names(ports)
				count = ports.count()
				return render(request,'aggregation/hubs.html',{'results':result,'site':name,'counter':count,'selected_option':agg_hub,'cascaded_option':cascaded,'status_option':status})
			except:
				name = f'{agg_hub} has NO {cascaded}'
				return render(request,'aggregation/hubs.html',{'site':name,'selected_option':agg_hub,'cascaded_option':cascaded,'status_option':status})
			
			# Searching by ports & Descipttions
	else:
		pass
	
	return render(request,'aggregation/hubs.html')

def aggsearch(request):
	if request.method =='POST':
		info = request.POST["search_desc"]
		agg_hub = request.POST["search_agg"]
		cascaded = request.POST["search_casc"]
		port = request.POST["search_port"]
		
		# searching by Port Description
		if info !='' and agg_hub !='' and cascaded !='':
			try:
				hub = agg(agg_hub)
				site = casc(cascaded,hub[0])
				ip = site[0]
				results = CascadedHubs.objects.filter(ip_address=ip,description__icontains=info).values()
				result = with_names(results)
				count =results.count()
				return render(request,'aggregation/search.html',{'results':result,'site':site[1],'counter':count,'search_desc':info,'selected_option':agg_hub,'cascaded_option':cascaded})	
			except:
				#name = f'Your Search has no results'
				#return render(request,'aggregation/search.html',{'site':name})
				pass
	
		elif info !='' and agg_hub !='' and cascaded =='':
		
			hub = agg(agg_hub)
			aggip = hub[0]
			ips = CascAggIps.objects.filter(agg_ip=hub[0])
			casc_ips=[val.ip_address for val in ips]
			result1 = AggregationHubs.objects.filter(ip_address=aggip,description__icontains=info).values()
			#result.append(result1)
			results = [i for i in result1]
			
			for ip in casc_ips:
				result2 = CascadedHubs.objects.filter(ip_address=ip,description__icontains=info).values()
				res =[i for i in result2]
				for k in res:
					results.append(k)
			result = with_names(results)
			count =len(results)
			return render(request,'aggregation/search.html',{'results':result,'counter':count,'search_desc':info,'selected_option':agg_hub})
		
		elif info !='' and agg_hub ==''and cascaded =='':
			result1 = AggregationHubs.objects.filter(description__icontains=info).values()
			results = [i for i in result1]
			result2 = CascadedHubs.objects.filter(description__icontains=info).values()
			res =[i for i in result2]
			for k in res:
				results.append(k)
			result = with_names(results)
			count =len(results)
			return render(request,'aggregation/search.html',{'results':result,'counter':count,'search_desc':info})
		else:
			pass
		
		# Searching by Port Number
		if port !='' and agg_hub !='' and cascaded !='':
			try:
				hub = agg(agg_hub)
				site = casc(cascaded,hub[0])
				ip = site[0]
				results = CascadedHubs.objects.filter(ip_address=ip,port__exact=port).values().exclude(description='10/100/Gig Ethernet TX')
				result = with_names(results)
				count =results.count()
				return render(request,'aggregation/search.html',{'results':result,'site':site[1],'counter':count,'search_port':port,'selected_option':agg_hub,'cascaded_option':cascaded})	
			except:
				name = f'Your Search has no results'
				return render(request,'aggregation/search.html',{'site':name})
	
		elif port !='' and agg_hub !=''and cascaded =='':
		
			hub = agg(agg_hub)
			aggip = hub[0]
			ips = CascAggIps.objects.filter(agg_ip=hub[0])
			casc_ips=[val.ip_address for val in ips]
			result1 = AggregationHubs.objects.filter(ip_address=aggip,port__exact=port).values()
			#result.append(result1)
			results = [i for i in result1]
			
			for ip in casc_ips:
				result2 = CascadedHubs.objects.filter(ip_address=ip,port__exact=port).values().exclude(description='10/100/Gig Ethernet TX')
				res =[i for i in result2]
				for k in res:
					results.append(k)
			result = with_names(results)
			count =len(results)
			return render(request,'aggregation/search.html',{'results':result,'counter':count,'search_port':port,'selected_option':agg_hub})
		
		elif port !='' and agg_hub ==''and cascaded =='':
			result1 = AggregationHubs.objects.filter(port__exact=port).values()
			results = [i for i in result1]
			result2 = CascadedHubs.objects.filter(port__exact=port).values().exclude(description='10/100/Gig Ethernet TX')
			res =[i for i in result2]
			for k in res:
				results.append(k)
			result = with_names(results)
			count =len(results)
			return render(request,'aggregation/search.html',{'results':result,'counter':count,'search_port':port})
		else:
			pass

		# No input to search by
		if info =='' and port =='':
			name = f'Enter atleast a Description or a Port you are searching by'
			return render(request,'aggregation/search.html',{'site':name})
	return render(request,'aggregation/search.html')

def aggedit(request):
	#Dedicating a port
	if request.method == 'POST':
		port = request.POST['edit_port']
		agghub = request.POST['edit_hub']
		cascaded = request.POST['edit_cascaded']
		description = request.POST['edit_description']

		if description !='':
			if port !='' and agghub !='' and cascaded !='':
				hub = agg(agghub)
				site = casc(cascaded,hub[0])
				ip = site[0]
				results = CascadedHubs.objects.filter(ip_address=ip,port__exact=port).values()
				try:
					status = results[0]['status']
					desc = results[0]['description']
				except:
					name = f'{cascaded} has NO port: {port}'
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'edit_port':port,'edit_description':description})
				
				if (status=='Free'or status == 'free') and (desc !='10/100/Gig Ethernet TX'):
					CascadedHubs.objects.filter(ip_address=ip,port=port).update(description=description,status='Used')
					name = f'You have changed {site[1]} port:{port} to {description}'
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'cascaded_option':cascaded,'edit_port':port,'edit_description':description})
				elif status =='Used' and desc != '10/100/Gig Ethernet TX':
					name = f'{site[1]} port:{port} is Used'
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'cascaded_option':cascaded,'edit_port':port,'edit_description':description})
				else:
					name = f"{port} isn't a fiber port. Choose from the range 1 to 6"
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'cascaded_option':cascaded,'edit_port':port,'edit_description':description})
			
			if port !='' and agghub !='' and cascaded =='':
				hub = agg(agghub)
				ip = hub[0]
				results = AggregationHubs.objects.filter(ip_address=ip,port__exact=port).values()
				try:
					status = results[0]['status']
					desc = results[0]['description']
				except:
					name = f'{agghub} has NO port: {port}'
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'edit_port':port,'edit_description':description})
				
				if (status=='Free'or status == 'free') and desc !='10/100/Gig Ethernet TX':
					AggregationHubs.objects.filter(ip_address=ip,port=port).update(description=description,status='Used')
					name = f'You have changed {hub[1]} port:{port} to {description}'
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'edit_port':port,'edit_description':description})
				elif status =='Used' and desc != '10/100/Gig Ethernet TX':
					name = f'{hub[1]} port:{port} is Used'
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'edit_port':port,'edit_description':description})
				else:
					name = f"{port} isn't a fiber port."
					return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'edit_port':port,'edit_description':description})
		else:
			name= f'Port Description can not be BLANK'
			return render(request,'aggregation/edit.html',{'site':name,'selected_option':agghub,'edit_port':port,'cascaded_option':cascaded})
		return render(request,'aggregation/edit.html')
	# Freeing a port
	return render(request,'aggregation/edit.html')

def aggfree(request):
	if request.method =='POST':
		agghub = request.POST['free-hub']
		port = request.POST['free-port']
		cascaded =request.POST["free-cascaded"]

		if port !='' and agghub !='' and cascaded !='':
			hub = agg(agghub)
			site = casc(cascaded,hub[0])
			ip = site[0]
			results = CascadedHubs.objects.filter(ip_address=ip,port__exact=port).values()
			try:
				status = results[0]['status']
				desc = results[0]['description']
			except:
				name = f'{cascaded} has NO port: {port}'
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'free_port':port,'cascaded_option':cascaded})
			if (status=='Used'or status == 'used') and desc !='10/100/Gig Ethernet TX':
				CascadedHubs.objects.filter(ip_address=ip,port=port).update(description="10/100/Gig Ethernet SFP",status='Free')
				name = f'You have changed {site[1]} port:{port} to Free'
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'cascaded_option':cascaded,'free-port':port})
			elif status =='Free' and desc != '10/100/Gig Ethernet TX':
				name = f'{site[1]} port:{port} is already Free'
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'cascaded_option':cascaded,'free-port':port})
			else:
				name = f"{port} isn't a fiber port. Choose from the range 1 to 6"
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'cascaded_option':cascaded,'free-port':port})
			
		if port !='' and agghub !='' and cascaded =='':
			hub = agg(agghub)
			ip = hub[0]
			results = AggregationHubs.objects.filter(ip_address=ip,port__exact=port).values()
			try:
				status = results[0]['status']
				desc = results[0]['description']
			except:
				name = f'{agghub} has NO port: {port}'
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'free_port':port})

			if (status=='Used'or status == 'used') and desc !='10/100/Gig Ethernet TX':
				AggregationHubs.objects.filter(ip_address=ip,port=port).update(description='10/100/Gig Ethernet SFP',status='Free')
				name = f'You have changed {hub[1]} port:{port} to Free'
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'free-port':port})
			elif status =='Free' and desc != '10/100/Gig Ethernet TX':
				name = f'{hub[1]} port:{port} is already Free'
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'free-port':port})
			else:
				name = f"{port} isn't a fiber port."
				return render(request,'aggregation/free.html',{'site':name,'selected_option':agghub,'free-port':port})
	return render(request,'aggregation/free.html')