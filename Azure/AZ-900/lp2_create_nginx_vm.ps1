az vm create --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --name my-vm --image UbuntuLTS --admin-username azureuser --generate-ssh-keys

az vm extension set --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --vm-name my-vm --name customScript --publisher Microsoft.Azure.Extensions --version 2.1 --settings '{"fileUris":["https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-nginx.sh"]}' --protected-settings '{"commandToExecute": "./configure-nginx.sh"}'

IPADDRESS="$(az vm list-ip-addresses --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --name my-vm --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" --output tsv)"

curl --connect-timeout 5 http://$IPADDRESS

echo $IPADDRESS

az network nsg list --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --query '[].name' --output tsv

az network nsg rule list --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --nsg-name my-vmNSG

az network nsg rule list --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --nsg-name my-vmNSG --query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' --output table

az network nsg rule create --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --nsg-name my-vmNSG --name allow-http --protocol tcp --priority 100 --destination-port-range 80 --access Allow

az network nsg rule list --resource-group learn-2621f747-ffd2-4eca-bb19-43ffb01d9efb --nsg-name my-vmNSG --query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' --output table

curl --connect-timeout 5 http://$IPADDRESS
